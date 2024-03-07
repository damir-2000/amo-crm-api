from abc import ABC, abstractmethod
from time import sleep
from typing import Literal, Optional, Union

from requests import Response, models, request

from ..exceptions import DoesNotExist, AuthenticationError


class BaseAuth(ABC):
    def __init__(self, subdomain: str) -> None:
        self._subdomain = subdomain
        self._api_v = "/api/v4"
        self._url = f"https://{self._subdomain}.amocrm.ru"

    def request(
        self,
        method: Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"],
        path: str = "",
        url: Optional[str] = None,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[Union[dict, list]] = None,
    ) -> Response:
        url = url + path if url else self._url + self._api_v + path
        sleep(0.2)
        response = request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            auth=self._auth,
            timeout=5,
        )
        
        if response.status_code == 404:
            raise DoesNotExist
        
        elif response.status_code == 401:
            raise AuthenticationError
        
        return response

    @abstractmethod
    def _auth(self, r: models.PreparedRequest) -> models.PreparedRequest:
        raise NotImplementedError
