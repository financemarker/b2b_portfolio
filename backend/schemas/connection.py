from pydantic import BaseModel, Field
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
