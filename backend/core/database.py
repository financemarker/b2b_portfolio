from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.core.config import settings


# Создаём движок (например, PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # проверяет соединение перед использованием
)

# Сессия для взаимодействия с БД
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass
