from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from backend.schemas.operation import Operation

# -----------------------------
# Общие модели
# -----------------------------
class Connection(BaseModel):
    connection_id: int
    account_id: int | None
    name: str
    broker_code: str
    status: str


# === PAYLOAD для создания подключения ===
class ConnectionCreate(BaseModel):
    """
    Payload для создания подключения.
    Передаётся в /users/{external_user_id}/connections/
    """
    broker_code: str = Field(..., example="tinkoff", description="Код брокера, например 'tinkoff' или 'finam'")
    strategy: str = Field(..., example="api", description="Тип стратегии: api, file, token, oauth2 и т.д.")
    name: Optional[str] = Field(None, example="Основной счёт", description="Имя подключения (опционально)")
    credentials: Optional[Dict[str, str]] = Field(
        None,
        description="Данные для подключения (токен, логин, пароль и т.п.)"
    )
    portfolio_id: Optional[int] = Field(
        None,
        description="Если нужно сразу привязать к существующему портфелю"
    )


class ImportPayload(BaseModel):
    """
    Универсальный payload для импорта операций.
    Используется в /users/{external_user_id}/imports/
    """
    connection_id: Optional[int] = Field(
        None,
        description="ID подключения (если импорт через существующий connection)"
    )
    operations: Optional[List[Operation]] = Field(
        None,
        description="Список операций (если импорт вручную или из файла)"
    )
    portfolio_id: Optional[int] = Field(
        None,
        description="Если нужно указать портфель явно"
    )
    external_user_id: Optional[str] = Field(
        None,
        description="Для внутренних вызовов можно дублировать ID пользователя (опционально)"
    )