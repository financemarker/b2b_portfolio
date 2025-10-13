from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.models.client import Client
from backend.schemas.client import ClientCreate, ClientRead

router = APIRouter()

@router.get("/", response_model=list[ClientRead])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).order_by(Client.id).all()

@router.post("/", response_model=ClientRead)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
