from backend.services.integration.brokers.base import BrokerBase

class TinkoffApi(BrokerBase):
    broker_code = "tinkoff"
    strategy = "api"
    supports_connections = True

    async def create_connections(self, **kwargs):
        # здесь логика, например, получения списка аккаунтов по токену
        token = kwargs.get("token") or kwargs.get("broker_token")
        if not token:
            raise Exception("Token not provided")

        # симуляция создания 2 подключений
        connections = [
            {"connection_id": 1, "account_id": "T123", "name": "Основной счёт", "status": "active"},
            {"connection_id": 2, "account_id": "T124", "name": "ИИС", "status": "active"},
        ]
        return connections

    async def import_operations(self, **kwargs):
        # пример получения операций из API (упрощённо)
        return [
            {"symbol": "AAPL", "qty": 10, "price": 170.5, "date": "2025-10-23"},
            {"symbol": "SBER", "qty": -5, "price": 250.0, "date": "2025-10-21"},
        ]
