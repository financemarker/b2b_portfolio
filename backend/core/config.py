from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from pathlib import Path


class Settings(BaseSettings):
    # ---- JWT / Security ----
    SECRET_KEY: str = Field(..., description="Секретный ключ для JWT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EPHEMERAL_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # === DATABASE CONFIG ===
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # === APP CONFIG ===
    DEBUG: bool = False
    ENV: str = "development"
    API_VERSION: str = "1.2"


    # === Pydantic 2.x config ===
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # === Derived field ===
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @field_validator("ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"ENV must be one of {allowed}")
        return v


settings = Settings()

print(
    f"✅ Loaded settings from .env: "
    f"{settings.POSTGRES_DB}@{settings.POSTGRES_HOST} (env={settings.ENV})"
)
