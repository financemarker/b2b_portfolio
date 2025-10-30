from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.dependencies import get_db, get_current_client
from backend.models.client import Client
from backend.models.user import User
from backend.models.connection import Connection
from backend.schemas.connection import ConnectionRead, ConnectionCreate, ImportPayload
from backend.schemas.response_wrapper import ApiResponse
from backend.schemas.operation import OperationCreate
from backend.services.integration import service
from backend.core import utils

router = APIRouter()

# === CONNECTIONS ===


@router.post("/{external_user_id}/connections/", response_model=ApiResponse[list[ConnectionRead]])
async def create_connection(
    external_user_id: str,
    payload: ConnectionCreate,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Создать новое подключение для пользователя"""
    try:
        result = await service.create_connection(db, client, external_user_id, payload)
        return ApiResponse.ok_list(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{external_user_id}/connections/", response_model=ApiResponse[list[ConnectionRead]])
async def get_connection(
    external_user_id: str,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Получить подключение"""
    user = db.query(User).filter(User.client_id == client.id, User.external_id == external_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    connections = db.query(Connection).filter(Connection.user_id == user.id).all()
    return ApiResponse.ok_list(connections)


# === IMPORTS ===
@router.post("/{external_user_id}/imports/", response_model=ApiResponse[list[OperationCreate]])
async def import_operations(
    external_user_id: str,
    payload: ImportPayload,
    db: Session = Depends(get_db),
    client: Client = Depends(get_current_client),
):
    """Разовый импорт сделок — по connection_id или файлу"""
    try:
        user = db.query(User).filter(User.client_id == client.id, User.external_id == external_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not payload.connection_id and not payload.operations:
            raise HTTPException(status_code=404, detail="Payload invalid: specify data for import")
        
        if not payload.portfolio_id:
            utils.check_portfolios_limit(client, user)

        result = await service.run_import(db, user, payload)
        return ApiResponse.ok_list(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
