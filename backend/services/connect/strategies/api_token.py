from backend.schemas.connect import ConnectResponse


class ApiTokenStrategy:
    def _build_portfolio(self, transactions):
        return ConnectResponse(broker_code=self.broker_code, transactions=transactions)
