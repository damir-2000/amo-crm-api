import json
import os
from typing import Optional

from .base import BaseTokenStorage


class FileTokenStorage(BaseTokenStorage):
    def __init__(self, directory_path=os.getcwd()):
        dir_path = os.path.join(directory_path, "tokens")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        self.access_token_path = os.path.join(
            directory_path, "tokens/access_token.json"
        )
        self.refresh_token_path = os.path.join(
            directory_path, "tokens/refresh_token.json"
        )

    @staticmethod
    def _read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as _file:
                return _file.read().strip()
        except FileNotFoundError:
            return None

    def get_access_token(self) -> Optional[str]:
        with open(file=self.access_token_path, mode="r", encoding="utf-8") as file:
            return json.load(file)["access_token"]

    def get_refresh_token(self) -> Optional[str]:
        with open(file=self.refresh_token_path, mode="r", encoding="utf-8") as file:
            return json.load(file)["refresh_token"]

    def save_tokens(self, access_token: str, refresh_token: str):
        with open(self.access_token_path, "w", encoding="utf-8") as _file:
            data = {"access_token": access_token}
            _file.write(json.dumps(data))

        with open(self.refresh_token_path, "w", encoding="utf-8") as _file:
            data = {"refresh_token": refresh_token}
            _file.write(json.dumps(data))
