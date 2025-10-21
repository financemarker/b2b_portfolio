from datetime import datetime
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.core.database import SessionLocal
from backend.models import Client
from backend.core.config import settings


# ---------- DB dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Auth dependency ----------
security = HTTPBearer(auto_error=False)

async def get_current_client(credentials: HTTPAuthorizationCredentials = Security(security),
                             db: Session = Depends(get_db)) -> Client:

    if not credentials:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = credentials.credentials

    # --- API Token ---
    if token.startswith("inpk_"):
        client = db.query(Client).filter(Client.api_token == token).first()
        if not client:
            raise HTTPException(status_code=401, detail="Invalid API token")
        if not client.valid_to or client.valid_to < datetime.today().date():
            raise HTTPException(
                status_code=403, detail="Client inactive or expired")
        return client

    # --- JWT Token ---
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        client_id = payload.get("client_id")
        if not client_id:
            raise HTTPException(
                status_code=401, detail="Invalid token payload")
        client = db.query(Client).get(client_id)
        if not client:
            raise HTTPException(status_code=401, detail="Client not active")
        return client
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired JWT")


def require_level(min_level: int):
    """Dependency для проверки минимального уровня роли (admin=10, pro=5, demo=1)"""
    def dependency(client: Client = Depends(get_current_client)):
        if not client or client.role.level < min_level:
            raise HTTPException(
                status_code=403, detail="Insufficient privileges")
        return client
    return dependency
