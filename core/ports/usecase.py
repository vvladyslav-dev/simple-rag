from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class UseCase(ABC, Generic[RequestT, ResponseT]):
    @abstractmethod
    def handle(self, request: RequestT) -> ResponseT:
        pass