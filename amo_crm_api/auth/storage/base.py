from abc import ABC, abstractmethod
from typing import Optional


class BaseTokenStorage(ABC):
    @abstractmethod
    def get_access_token(self) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_refresh_token(self) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def save_tokens(self, access_token: str, refresh_token: str):
        raise NotImplementedError
