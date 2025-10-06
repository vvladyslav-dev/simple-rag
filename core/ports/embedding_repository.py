from abc import ABC, abstractmethod
from typing import Any

class EmbeddingRepository(ABC):
    @abstractmethod
    def embed(self, text: str) -> Any:
        pass