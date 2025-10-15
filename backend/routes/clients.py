from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.dependencies import get_db, get_current_client, require_level
from backend.models.client import Client
from backend.schemas.client import ClientCreate, ClientRead
from backend.schemas.response_wrapper import ApiResponse
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=ApiResponse[list[ClientRead]], dependencies=[Depends(require_level(10))])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).order_by(Client.id).all()
    data = [ClientRead.model_validate(c) for c in clients]
    return ApiResponse.ok_list(data)


@router.get("/me", response_model=ApiResponse[ClientRead])
def get_me(client=Depends(get_current_client)):
    data = ClientRead.model_validate(client)
    return ApiResponse.ok_item(data)


@router.post("/", response_model=ApiResponse[ClientRead], responses={422: {"description": "Validation error", "model": ApiResponse[None]}})
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    client = Client(
        email=data.email,
        password_hash=pwd_context.hash(data.password_hash),
        role_code=data.role_code
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    client_read = ClientRead.model_validate(client)
    return ApiResponse.ok_item(client_read)
