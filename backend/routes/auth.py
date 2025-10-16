from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.core.dependencies import get_db
from backend.models import Client
from backend.core.config import settings
from backend.schemas.response_wrapper import ApiResponse
from backend.schemas.auth import TokenResponse, LoginRequest, RefreshRequest

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Helpers ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + expires_delta
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_days: int) -> str:
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["exp"] = datetime.now() + timedelta(days=expires_days)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ---------- Routes ----------
@router.post("/login", response_model=ApiResponse[TokenResponse], responses={422: {"description": "Validation error", "model": ApiResponse[None]}})
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Авторизация клиента по email + пароль"""
    client = db.query(Client).filter(Client.email == data.email).first()
    if not client or not verify_password(data.password, client.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")

    access_token = create_access_token(
        {"client_id": client.id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        {"client_id": client.id},
        settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    token_data = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        role=client.role_code
    )
    return ApiResponse.ok_item(token_data)


@router.post("/refresh", response_model=ApiResponse[TokenResponse], responses={422: {"description": "Validation error", "model": ApiResponse[None]}})
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    """Обновление access-токена"""
    try:
        payload = jwt.decode(data.refresh_token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
        client_id = payload.get("client_id")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(401, "Client not found or inactive")

    access_token = create_access_token(
        {"client_id": client.id},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    token_data = TokenResponse(access_token=access_token)
    return ApiResponse.ok_item(token_data)
