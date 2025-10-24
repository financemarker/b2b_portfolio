from typing import List
from sqlalchemy.orm import Session
from backend.models import User, Portfolio, Connection
from backend.core import utils
from .brokers.tinkoff_token import TinkoffApi
# сюда же будут добавляться другие брокеры

# === Централизованный реестр брокеров ===
BROKER_REGISTRY = {
    "tinkoff_api": TinkoffApi(),
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

    user, _ = utils.get_or_create(db, User, client_id=client.id, external_id=external_user_id)

    # вызывем брокера
    raw_connections = await broker.create_connections(**payload.model_dump())

    created = []
    for conn in raw_connections:
        connection = Connection(
            user_id=user.id,
            broker_code=payload.broker_code,
            strategy=payload.strategy,
            name=conn.get("name"),
            status=conn.get("status", "active"),
            credentials=conn,
        )
        db.add(connection)
        db.commit()
        db.refresh(connection)
        created.append(connection)
    return created


async def run_import(db: Session, client, external_user_id: str, payload):
    """
    Импорт операций:
    - если указан connection_id → используем существующее соединение
    - если operations → обрабатываем как file/manual импорт
    """
    user, _ = utils.get_or_create(db, User, client_id=client.id, external_id=external_user_id)

    # Получаем брокера
    if payload.connection_id:
        connection = db.query(Connection).filter_by(id=payload.connection_id, user_id=user.id).first()
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

