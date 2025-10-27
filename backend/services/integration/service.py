from typing import List
from sqlalchemy.orm import Session
from backend.models import User, Portfolio, Connection
from backend.core import utils
from backend.services.integration.brokers.tinkoff_token import TinkoffToken
# сюда же будут добавляться другие брокеры

# === Централизованный реестр брокеров ===
BROKER_REGISTRY = {
    "tinkoff_token": TinkoffToken(),
    # "finam_file": FinamFile(),
}

# === Фасад для маршрутов ===


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


async def run_import(db: Session, client, external_user_id: str, payload):
    """
    Импорт операций:
    - если указан connection_id → используем существующее соединение
    - если operations → обрабатываем как file/manual импорт
    """
    user, _ = utils.get_or_create(
        db, User, client_id=client.id, external_id=external_user_id)

    # Получаем брокера
    if payload.connection_id:
        connection = db.query(Connection).filter_by(
            id=payload.connection_id, user_id=user.id).first()
        if not connection:
            raise Exception("Connection not found")

        broker_key = f"{connection.broker_code}_{connection.strategy}"
        broker = BROKER_REGISTRY.get(broker_key)
        if not broker:
            raise Exception(f"Broker '{broker_key}' not registered")

        operations = await broker.import_operations(**payload.model_dump())
    else:
        # ручной / file импорт
        operations = payload.operations or []

    # тут можно сохранить операции в таблицу `operations`
    # (в примере просто возвращаем список)
    return operations
