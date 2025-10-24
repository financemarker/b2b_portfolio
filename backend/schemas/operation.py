from pydantic import BaseModel, Field
from typing import Optional


# -----------------------------
# Payload для ручного ввода сделок и токенов
# -----------------------------
class OperationCreate(BaseModel):
    """Одна сделка для ручного импорта."""
    symbol: str = Field(..., description="Тикер инструмента, например 'AAPL'")
    qty: float = Field(..., description="Количество бумаг (может быть отрицательным при продаже)")
    price: float = Field(..., description="Цена за единицу инструмента")
    date: Optional[str] = Field(None, description="Дата сделки в формате YYYY-MM-DD")
