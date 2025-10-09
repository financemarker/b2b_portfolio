from pydantic import BaseModel, EmailStr
from datetime import datetime

# Базовая схема
class UserBase(BaseModel):
    name: str
    email: EmailStr

# Для создания
class UserCreate(UserBase):
    pass

# Для возврата
class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # позволяет FastAPI читать ORM-объекты
