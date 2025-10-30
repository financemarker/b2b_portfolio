from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from backend.schemas.operation import OperationCreate
from backend.models.connection import ConnectionStatus

# -----------------------------
# Общие модели
# -----------------------------
class ConnectionRead(BaseModel):
    id: int
    access_token: str | None
    account_id: int | None
    name: str
    broker_code: str
    strategy: str
    status: ConnectionStatus


# === PAYLOAD для создания подключения ===
class ConnectionCreate(BaseModel):
    """
    Payload для создания подключения.
    Передаётся в /users/{external_user_id}/connections/
    """
    broker_code: str = Field(..., example="tinkoff", description="Код брокера, например 'tinkoff' или 'finam'")
    strategy: str = Field(..., example="token", description="Тип стратегии: api, file, token, oauth2 и т.д.")
    access_token: str | None = Field(None, description="Токен доступа для чтения сделок")


class ImportPayload(BaseModel):
    """
    Универсальный payload для импорта операций.
    Используется в /users/{external_user_id}/imports/
    """
    connection_id: int | None = Field(None, description="ID подключения (если импорт через существующий connection)")
    operations: List[OperationCreate] | None = Field(None, description="Список операций (если импорт вручную или из файла)")
    portfolio_id: int | None = Field(None, description="ID портфеля для сохранения операций. Если не указан - создается автоматически")