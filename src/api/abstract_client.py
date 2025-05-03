from requests import Response

from abc import ABC, abstractmethod, abstractproperty


class AbstractClient(ABC):
    @abstractmethod
    def get(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def post(self) -> Response:
        raise NotImplementedError
