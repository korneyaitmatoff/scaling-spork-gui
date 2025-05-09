from typing import Any

from requests import Session, Response

from src.api.abstract_client import AbstractClient


class BaseClient(AbstractClient):
    url: str

    def __init__(self, url: str):
        self.url = url

    def get(self, path: str = "/", **kwargs) -> Response:
        return Session().get(
            url=self.url + path,
            **kwargs
        )

    def post(self, path: str = "/", data: dict[str, Any] = None, json: dict[str, Any] = None, **kwargs) -> Response:
        session = Session()

        return session.post(
            url=self.url + path,
            data=data,
            json=json,
            **kwargs
        )
