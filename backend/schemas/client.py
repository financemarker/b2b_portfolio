from pydantic import BaseModel, EmailStr
from datetime import date

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
    api_token: str
    valid_to: date
    users_limit: int | None
    users_count: int
    user_portfolios_limit: int | None
    api_requests_limit: int | None
    api_requests_remaining: int | None

    class Config:
        from_attributes = True  # позволяет FastAPI читать ORM-объекты
