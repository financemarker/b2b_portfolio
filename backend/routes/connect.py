from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from datetime import datetime, timedelta
from jose import jwt
from backend.core.dependencies import get_current_client
from backend.schemas.connect import ConnectPayload, TokenRequest, ConnectResponse, EphemeralLink
from backend.schemas.response_wrapper import ApiResponse
from backend.services.connect import service
from backend.core.config import settings

router = APIRouter()


def create_ephemeral_token(tenant_id: str, broker_code: str, external_id: str | None = None) -> str:
    """
    Создаёт короткоживущий JWT для инициализации OAuth-сессии.
    Токен живёт 10 минут и используется для генерации временной authorize-ссылки.
    """
    payload = {
        "tenant_id": tenant_id,
        "broker_code": broker_code,
        "external_id": external_id,
        "exp": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# -----------------------------
# 1️⃣ Универсальный endpoint для file/api_token/manual
# -----------------------------
@router.post("/{broker_code}/{strategy}", response_model=ApiResponse[ConnectResponse], responses={422: {"description": "Validation error", "model": ApiResponse[None]}})
async def connect_broker(
    broker_code: str,
    strategy: str,
    client=Depends(get_current_client),
    data: ConnectPayload | None = None,
    file: UploadFile | None = File(None),
):
    try:
        payload = data.model_dump(exclude_none=True) if data else {}
        if file:
            payload["file"] = file

        broker_id = f"{broker_code}_{strategy}"
        result = await service.handle_connect(broker_id, payload)
        return ApiResponse.ok_item(result)

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# -----------------------------
# 2️⃣ Инициализация OAuth2 (создание временной ссылки)
# -----------------------------
@router.post(
    "/token",
    response_model=ApiResponse[EphemeralLink],
    responses={422: {"description": "Validation error",
                     "model": ApiResponse[None]}},
    summary="Создание временного токена для OAuth2",
    description="Генерирует link-токен и ссылку для авторизации брокера через OAuth2.",
)
async def create_oauth_link(data: TokenRequest, client=Depends(get_current_client)):
    try:
        token = create_ephemeral_token(
            tenant_id=data.tenant_id,
            broker_code=data.broker_code,
            external_id=data.external_id,
        )
        authorize_url = f"https://inport.app/v1/connect/authorize?token={token}"
        ephemeral_link = EphemeralLink(
            authorize_url=authorize_url, token=token)
        return ApiResponse.ok_item(ephemeral_link)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# -----------------------------
# 3️⃣ Callback от брокера (OAuth2)
# -----------------------------
@router.get(
    "/callback/{broker_code}/{strategy}",
    response_model=ApiResponse[ConnectResponse],
    responses={422: {"description": "Validation error",
                     "model": ApiResponse[None]}},
    summary="Callback от брокера (OAuth2)",
    description="Обрабатывает redirect от брокера после успешной OAuth-авторизации.",
)
async def oauth_callback(broker_code: str, strategy: str, code: str, state: str | None = None):
    """
    Обрабатывает redirect от брокера после успешного OAuth2 логина.
    """
    try:
        broker_id = f"{broker_code}_{strategy}"
        result = await service.handle_connect(broker_id, {"code": code, "state": state})
        return ApiResponse.ok_item(result)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
