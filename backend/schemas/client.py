from pydantic import BaseModel, EmailStr
from datetime import datetime

# Базовая схема
class ClientBase(BaseModel):
    email: EmailStr
    password_hash: str
    role_code: str

# Для создания
class ClientCreate(ClientBase):
    pass

# Для возврата
class ClientRead(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # позволяет FastAPI читать ORM-объекты
