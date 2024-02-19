from datetime import datetime
from typing import Optional, TypedDict

import jwt
from requests import request

from .base import BaseAuth
from .storage import BaseTokenStorage, FileTokenStorage


class TokensDict(TypedDict):
    access_token: str
    refresh_token: str


class AmoCRMAuth(BaseAuth):
    def __init__(
        self,
        subdomain: str,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        storage: BaseTokenStorage = FileTokenStorage(),
    ) -> None:
        self._storage = storage
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_url = redirect_url
        super().__init__(subdomain)

    def _auth(self, r):
        r.headers["Authorization"] = f"Bearer {self._get_access_token()}"
        return r

    def init(self, code: str, skip_error: bool = False):
        data = self._get_or_update_tokens(code=code, skip_error=skip_error)
        if not data:
            return
        self._storage.save_tokens(data["access_token"], data["refresh_token"])

    def _update_tokens(self) -> str:
        refresh_token = self._storage.get_refresh_token()

        data = self._get_or_update_tokens(refresh_token=refresh_token)
        if not data:
            raise
        self._storage.save_tokens(data["access_token"], data["refresh_token"])
        return data["access_token"]

    def _get_or_update_tokens(
        self,
        refresh_token: Optional[str] = None,
        code: Optional[str] = None,
        skip_error: bool = False,
    ) -> Optional[TokensDict]:
        url = f"{self._url}/oauth2/access_token"
        data = dict(
            client_id=self._client_id,
            client_secret=self._client_secret,
            redirect_uri=self._redirect_url,
        )

        if refresh_token:
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = refresh_token
        elif code:
            data["grant_type"] = "authorization_code"
            data["code"] = code
        else:
            raise

        response = request(method="POST", url=url, json=data)

        if response.status_code != 200 and not skip_error:
            raise Exception(response.json()["hint"])
        if response.status_code != 200 and skip_error:
            return None

        return response.json()

    def _get_access_token(self) -> Optional[str]:
        access_token = self._storage.get_access_token()
        if not access_token:
            raise EnvironmentError("You need to init tokens with code by 'init' method")
        if self._is_expire(access_token):
            access_token = self._update_tokens()

        return access_token

    @staticmethod
    def _is_expire(access_token: str) -> bool:
        token_data = jwt.decode(access_token, options={"verify_signature": False})
        exp = datetime.utcfromtimestamp(token_data["exp"])
        now = datetime.utcnow()
        return now >= exp
