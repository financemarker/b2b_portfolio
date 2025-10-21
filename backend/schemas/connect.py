from pydantic import BaseModel, Field
from typing import Optional, List


# -----------------------------
# Общие модели
# -----------------------------
class ConnectResponse(BaseModel):
    portfolio_id: int
    broker_code: str
    status: str

# -----------------------------
# Payload для ручного ввода сделок и токенов
# -----------------------------
class Trade(BaseModel):
    """Одна сделка для ручного импорта."""
    symbol: str = Field(..., description="Тикер инструмента, например 'AAPL'")
    qty: float = Field(..., description="Количество бумаг (может быть отрицательным при продаже)")
    price: float = Field(..., description="Цена за единицу инструмента")
    date: Optional[str] = Field(None, description="Дата сделки в формате YYYY-MM-DD")


class ConnectPayload(BaseModel):
    """
    Универсальный payload для подключения брокера.

    Поддерживаемые сценарии:
    - Передача списка сделок (`trades`) для ручного импорта;
    - Передача `broker_token` для API-интеграции;
    - File
    """
    trades: Optional[List[Trade]] = Field(None, description="Список сделок для ручного импорта")
    broker_token: Optional[str] = Field(None, description="API токен брокера")
    external_user_id: str = Field(..., description="Идентификатор пользователя в системе клиента")


# -----------------------------
# Запрос для OAuth link-токена
# -----------------------------
class TokenRequest(BaseModel):
    tenant_id: str = Field(..., description="Идентификатор клиента (B2B клиент или приложение)")
    broker_code: str = Field(..., description="Код брокера (например 'ibkr')")
    external_user_id: str = Field(..., description="Идентификатор пользователя в системе клиента")

class EphemeralLink(BaseModel):
    authorize_url: str = Field(..., description="Ссылка авторизации")
    token: str = Field(..., description="Кратковременный токен")
