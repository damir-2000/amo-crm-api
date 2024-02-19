from .base import BaseAuth


class AmoCRMTokenAuth(BaseAuth):
    def __init__(self, subdomain: str, token: str) -> None:
        self._token = token
        super().__init__(subdomain)

    def _auth(self, r):
        r.headers["Authorization"] = f"Bearer {self._token}"
        return r
