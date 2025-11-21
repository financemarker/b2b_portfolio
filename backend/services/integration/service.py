from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.models import User, Portfolio, Connection, PortfolioConnection
from backend.core import utils
from backend.services.integration.brokers.tinkoff_token import TinkoffToken
from backend.schemas.portfolio import ImportResponse
# сюда же будут добавляться другие брокеры

# === Централизованный реестр брокеров ===
BROKER_REGISTRY = {
    "tinkoff_token": TinkoffToken(),
    # "manual_json": ManualJson(),
    # "finam_file": FinamFile(),
}


async def create_connection(db: Session, client, external_user_id: str, payload) -> List[dict]:
    """
    1. Резолвит пользователя по external_user_id
    2. Вызывает брокера для создания connections
    3. Сохраняет их в таблицу connections и возвращает список
    """
    broker_key = f"{payload.broker_code}_{payload.strategy}"
    broker = BROKER_REGISTRY.get(broker_key)
    if not broker:
        raise Exception(f"Broker '{broker_key}' not found")

    user, creation_flag = utils.get_or_create(
        db, User, client_id=client.id, external_id=external_user_id)

    # вызывем брокера
    broker_accounts = await broker.get_accounts(**payload.model_dump())

    connections = []
    for account in broker_accounts:
        connection = Connection(
            user_id=user.id,
            broker_code=payload.broker_code,
            strategy=payload.strategy,
            name=account.get("name"),
            access_token=payload.access_token,
            account_id=account.get("id"),
            status=account.get("status")
        )
        db.add(connection)
        db.commit()
        db.refresh(connection)
        connections.append(connection)
    return connections


async def import_operations(db: Session, user, portfolio, payload) -> ImportResponse:
    import_results = {}
    # Получаем операции от брокера или из payload
    connection = None
    if payload.connection_id:
        connection = db.query(Connection).filter_by(
            id=payload.connection_id, user_id=user.id).first()
        if not connection:
            raise Exception("Connection not found")
        broker_key = f"{connection.broker_code}_{connection.strategy}"

        utils.link_portfolio_with_connection(db, portfolio, connection)
    else:
        broker_key = "manual_json"

    broker = BROKER_REGISTRY.get(broker_key)
    if not broker:
        raise Exception(f"Integration for '{broker_key}' not found")

    

    # Prepare kwargs for broker's import_operations method
    import_kwargs = {
        "connection": connection,
        "portfolio": portfolio,
        "operations": payload.operations,
        "db": db,
    }

    # Get operations from broker
    operations = await broker.import_operations(**import_kwargs)
    # batch save and prepare results stat
    

    return import_results
