from abc import ABC, abstractmethod
from typing import Any

class DocumentLoader(ABC):
    @abstractmethod
    def load(self) -> list[Any]:
        pass
