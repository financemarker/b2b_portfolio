import sys
from fastapi import FastAPI
from pathlib import Path

# Загружаем .env
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.routes import clients

app = FastAPI(title="B2B Portfolio")
app.include_router(clients.router, prefix="/v1/clients", tags=["clients"])
