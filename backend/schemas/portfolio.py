from pydantic import BaseModel, Field
from typing import List
from backend.schemas.operation import OperationCreate

# -----------------------------
# Payload для ручного ввода сделок и токенов
# -----------------------------
class PortfolioBase(BaseModel):
    """Base Schema for portfolio"""


class PortfolioRead(PortfolioBase):
    """Read Schema for portfolio"""


class PortfolioCreate(PortfolioBase):
    """Create Schema for portfolio"""


class ImportPayload(BaseModel):
    """
    Универсальный payload для импорта операций.
    Используется в /users/{external_user_id}/imports/
    """
    external_user_id: str = Field(..., description="Внешний ид юзера")
    connection_id: int | None = Field(None, description="ID подключения (если импорт через существующий connection)")
    operations: List[OperationCreate] | None = Field(None, description="Список операций (если импорт вручную или из файла)")
    portfolio_id: int | None = Field(None, description="ID портфеля для сохранения операций. Если не указан - создается автоматически")



class ImportResponse(BaseModel):
    """
    Универсальный payload для импорта операций.
    Используется в /users/{external_user_id}/imports/
    """
    warnings: List[dict]
    operations: List[OperationCreate] | None = Field(None, description="Список операций (если импорт вручную или из файла)")
    total: int
    total_imported: int
