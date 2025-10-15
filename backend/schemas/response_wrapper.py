from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar, Sequence
from pydantic import BaseModel, Field, model_serializer
from backend.core.config import settings

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Модель для описания ошибок API."""
    code: int = Field(..., description="HTTP-код или внутренний код ошибки")
    message: str = Field(..., description="Описание ошибки для клиента")

    model_config = {
        "from_attributes": True,
    }


class MetaResponse(BaseModel):
    """Дополнительная информация об ответе (например, пагинация, версия API)."""
    page: Optional[int] = Field(None, description="Номер текущей страницы")
    per_page: Optional[int] = Field(None, description="Размер страницы")
    total: Optional[int] = Field(None, description="Всего элементов")
    timestamp: Optional[datetime] = Field(
        None, description="Время формирования (ISO)")
    version: Optional[str] = Field(None, description="Версия API")

    @classmethod
    def auto(cls, **kwargs) -> "MetaResponse":
        """Создаёт meta с автозаполнением timestamp и версии."""
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(
                timespec="milliseconds"),
            version=getattr(settings, "API_VERSION", "1.0"),
            **kwargs,
        )

    @model_serializer(mode="wrap")
    def _serialize(self, handler):
        data = handler(self)          # стандартная сериализация в dict
        return {k: v for k, v in data.items() if v is not None}

    model_config = {
        "from_attributes": True,
        "exclude_none": True,
    }


class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(None, description="Основные данные ответа")
    error: Optional[ErrorResponse] = Field(
        None, description="Информация об ошибке, если есть", examples=[None])
    meta: Optional[MetaResponse] = Field(
        None, description="Дополнительные данные", examples=[None])

    @classmethod
    def ok_item(cls, item: T) -> "ApiResponse[T]":
        return cls(data=item)

    @classmethod
    def ok_list(cls, items: Sequence[T], **meta_kwargs) -> "ApiResponse[list[T]]":
        """
        Быстрый ответ для списка объектов (с опциональной пагинацией).
        Пример:
            ApiResponse.ok_list(items, page=1, per_page=20, total=256)
        """
        return cls(data=list(items), meta=MetaResponse(**meta_kwargs))

    @classmethod
    def fail(cls, code: int, message: str) -> "ApiResponse[T]":
        return cls(data=None, meta=MetaResponse.auto(), error=ErrorResponse(code=code, message=message))

    model_config = {
        "from_attributes": True,
    }
