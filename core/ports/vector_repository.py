from abc import ABC, abstractmethod
from langchain_core.documents import Document
from typing import Any
from qdrant_client.conversions import common_types as types

class VectorRepository(ABC):
    @abstractmethod
    def similarity_search_by_vector(self, collection_name: str, vector: list[float], k: int = 5) -> list[Document]:
        pass

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> None:
        pass

    @abstractmethod
    def add_vectors(self, collection_name: str, vectors_with_docs: list[tuple[Any, Document]]) -> None:
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int) -> None:
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def get_collections_list(self) -> types.CollectionsResponse:
        pass