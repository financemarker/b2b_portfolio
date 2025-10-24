from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.dependencies import get_db, get_current_client
from backend.models.client import Client
from backend.models.user import User
from backend.models.connection import Connection
from backend.schemas.connection import Connection, ConnectionCreate, ImportPayload
from backend.schemas.response_wrapper import ApiResponse
from backend.services.integration import service

router = APIRouter()

# === CONNECTIONS ===


@router.post("/{external_user_id}/connections/", response_model=ApiResponse[list[Connection]])
async def create_connection(
    external_user_id: str,
    payload: ConnectionCreate,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Создать новое подключение для пользователя"""
    try:
        result = await service.create_connection(db, client, external_user_id, payload)
        return ApiResponse.ok(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{external_user_id}/connections/", response_model=ApiResponse[list[Connection]])
async def get_connection(
    external_user_id: str,
    connection_id: int,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Получить подключение"""
    user = db.query(User).filter(external_id=external_user_id)
    connections = db.query(Connection).filter(user_id=user.id)
    if not connections:
        raise HTTPException(status_code=404, detail="Connection not found")
    return ApiResponse.ok_list(connections)


# === IMPORTS ===
@router.post("/{external_user_id}/imports/", response_model=ApiResponse)
async def import_operations(
    external_user_id: str,
    payload: ImportPayload,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Разовый импорт сделок — по connection_id или файлу"""
    try:
        result = await service.run_import(db, client, external_user_id, payload)
        return ApiResponse.ok(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
