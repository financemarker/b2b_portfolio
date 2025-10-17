import sys
from fastapi import FastAPI
from pathlib import Path
from backend.core.exceptions import register_exception_handlers
from backend.routes import clients, auth, connect

# Загружаем .env
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = FastAPI(title="B2B Portfolio")
register_exception_handlers(app)

app.include_router(connect.router, prefix="/v1/connect", tags=["connect"])
app.include_router(clients.router, prefix="/v1/clients", tags=["clients"])
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
