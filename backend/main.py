import sys
from fastapi import FastAPI
from pathlib import Path
from backend.core.exceptions import register_exception_handlers
from backend.routes import clients, auth, ext_users, portfolios

# Загружаем .env
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = FastAPI(title="B2B Portfolio")
register_exception_handlers(app)

app.include_router(ext_users.router, prefix="/v1/external_users", tags=["ext_users"])
app.include_router(portfolios.router, prefix="/v1/portfolios", tags=["portfolios"])
app.include_router(clients.router, prefix="/v1/clients", tags=["clients"])
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
