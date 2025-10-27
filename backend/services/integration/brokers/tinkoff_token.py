from tinkoff.invest import Client, GetOperationsByCursorRequest
from tinkoff.invest.constants import INVEST_GRPC_API
from datetime import datetime
import time
import json
from backend.services.integration.brokers.base import BrokerBase, AccountDict
from backend.models.connection import ConnectionStatus


class TinkoffToken(BrokerBase):
    broker_code = "tinkoff"
    strategy = "api"
    supports_connections = True

    # Получение списка портфелей по токену
    async def get_accounts(self, **kwargs) -> list[AccountDict]:
        # здесь логика, например, получения списка аккаунтов по токену
        token = kwargs.get("access_token")
        if not token:
            raise Exception("Token not provided")

        with Client(token, target=INVEST_GRPC_API) as client:
            try:
                getAccountsRes = client.users.get_accounts()
                accounts = []
                for account in getAccountsRes.accounts:
                    if account.access_level.name != 'ACCOUNT_ACCESS_LEVEL_READ_ONLY':
                        raise Exception("We only allow read access tokens")
                    accounts.append({
                        'id': account.id,
                        'name': account.name,
                        'status': ConnectionStatus.ACTIVE 
                    })
            except Exception as e:
                raise Exception(e.metadata.message)

        return accounts

    async def import_operations(self, **kwargs):
        # пример получения операций из API (упрощённо)
        return [
            {"symbol": "AAPL", "qty": 10, "price": 170.5, "date": "2025-10-23"},
            {"symbol": "SBER", "qty": -5, "price": 250.0, "date": "2025-10-21"},
        ]
