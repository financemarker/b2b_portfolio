from pydantic import BaseModel, EmailStr
from datetime import datetime

# Базовая схема
class ClientBase(BaseModel):
    email: EmailStr
    role_code: str

# Для создания
class ClientCreate(ClientBase):
    password: str

# Для возврата
class ClientRead(ClientBase):
    id: int

    class Config:
        from_attributes = True  # позволяет FastAPI читать ORM-объекты
