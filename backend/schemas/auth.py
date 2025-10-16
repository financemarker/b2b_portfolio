from pydantic import BaseModel, model_serializer, EmailStr

class RefreshRequest(BaseModel):
    refresh_token: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    role: str | None = None

    model_config = {
        "from_attributes": True,
        "exclude_none": True,
    }

    @model_serializer(mode="wrap")
    def _serialize(self, handler):
        data = handler(self)          # стандартная сериализация в dict
        return {k: v for k, v in data.items() if v is not None}