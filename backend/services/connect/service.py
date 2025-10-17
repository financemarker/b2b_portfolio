from backend.schemas.connect import ConnectResponse
from backend.services.connect.brokers.tinkoff_api import TinkoffApi
from backend.services.connect.brokers.mock_file import MockFile

# 🔹 Минимальный и прозрачный реестр
BROKER_REGISTRY = {
    "tinkoff_api": TinkoffApi(),
    "mock_file": MockFile(),
}


def handle_connect(broker_code: str, payload: dict) -> ConnectResponse:
    """Основная точка входа: вызывает нужный брокер."""
    broker = BROKER_REGISTRY.get(broker_code)
    if not broker:
        raise Exception(f"Broker '{broker_code}' not found")

    result = broker.connect(**payload)

    if not isinstance(result, (dict, ConnectResponse)):
        raise Exception("Invalid response format")

    return result
