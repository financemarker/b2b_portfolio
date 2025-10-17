import requests
from backend.schemas.connect import ConnectResponse


class ApiTokenStrategy:
    def request(self, endpoint: str, token: str, params=None):
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base_url}/{endpoint}", headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def _build_portfolio(self, transactions):
        return ConnectResponse(broker_code=self.broker_code, transactions=transactions)
