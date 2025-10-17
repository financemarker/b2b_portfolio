import requests
from backend.schemas.connect import ConnectResponse


class OAuthStrategy:
    def get_auth_url(self):
        return f"{self.auth_url}?client_id={self.client_id}&scope={self.scope}"

    def exchange_code(self, code: str):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        resp = requests.post(self.token_url, data=data)
        resp.raise_for_status()
        return resp.json()

    def _build_portfolio(self, transactions):
        return ConnectResponse(broker_code=self.broker_code, transactions=transactions)
