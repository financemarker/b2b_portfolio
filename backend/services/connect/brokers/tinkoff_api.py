from backend.services.connect.strategies.api_token import ApiTokenStrategy


class TinkoffApi(ApiTokenStrategy):
    broker_code = "tinkoff"
    strategy_type = "api_token"
    base_url = "https://api-invest.tinkoff.ru/openapi"

    def connect(self, api_token, context=None):
        data = self.request("operations", api_token)
        # упрощённая нормализация
        transactions = [
            {"symbol": x["figi"], "qty": x["quantity"], "price": x["price"]}
            for x in data.get("operations", [])
        ]
        return self._build_portfolio(transactions)
