import sys
from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env
sys.path.append(str(Path(__file__).resolve().parent.parent))
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


from backend.database import Base, engine
from backend.routes import users

# Инициализируем БД (создаём таблицы, если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inport API")
app.include_router(users.router, prefix="/v1/users", tags=["users"])
