from sqlalchemy.orm import Session
from backend.schemas.connect import ConnectResponse
from backend.services.connect.brokers.tinkoff_token import TinkoffToken
from backend.services.connect.brokers.finam_file import FinamFile
from backend.models import Client, Portfolio, User
from backend.core import utils

# 🔹 Минимальный и прозрачный реестр
BROKER_REGISTRY = {
    "tinkoff_token": TinkoffToken(),
    "finam_file": FinamFile(),
}

async def handle_connect(db: Session, client: Client, broker_code: str, payload: dict) -> ConnectResponse:
    """Основная точка входа: вызывает нужный брокер."""
    broker = BROKER_REGISTRY.get(broker_code)
    if not broker:
        raise Exception(f"Broker integration '{broker_code}' not found")

    # get user - mandatory field
    user, creation_flag = utils.get_or_create(db, User, client_id = client.id, external_id = payload["external_user_id"])

    # get and check portfolio
    if "portfolio_id" in payload:
        portfolio = db.query(Portfolio).filter(Portfolio.id == payload["portfolio_id"]).first()
        if not portfolio or user.id != portfolio.user_id:   
            raise Exception(f"Portfolio with id '{payload["portfolio_id"]}' for user '{payload["external_user_id"]}' not found")
    else:
        portfolio = Portfolio(user_id = user.id, broker_code = broker_code, name = f"{broker_code} portfolio")
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        payload["portfolio_id"] = portfolio.id

    status = await broker.connect(**payload)

    return ConnectResponse(portfolio_id=int(payload["portfolio_id"]), broker_code=broker_code, status=status)
