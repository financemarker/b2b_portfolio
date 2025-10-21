from backend.services.connect.strategies.api_token import ApiTokenStrategy


class TinkoffToken(ApiTokenStrategy):
    base_url = "https://api-invest.tinkoff.ru/openapi"

    async def connect(self, portfolio_id, broker_token, **kwargs):
        data = []
        # упрощённая нормализация
        transactions = [
            {"symbol": x["figi"], "qty": x["quantity"], "price": x["price"]}
            for x in data
        ]
        return 'success'
