import os
import logging
import uuid
from qdrant_client import QdrantClient
from core.ports.vector_repository import VectorRepository
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_core.documents import Document
from typing import Any
from qdrant_client.conversions import common_types as types

class QdrantRepository(VectorRepository):
    def __init__(self):
        # Prefer Docker service URL if running inside docker-compose network
        qdrant_url = os.getenv("QDRANT_URL", "http://qdrant:6333")
        self.client = QdrantClient(qdrant_url)
        self._logger = logging.getLogger(self.__class__.__name__)
        # Embedding is intentionally not stored here to keep infra free of domain logic.

    def add_documents(self, documents):
        pass
        # return self.store.add_documents(documents)

    def similarity_search_by_vector(self, collection_name: str, vector: list[float], k: int = 5):
        # Ensure collection exists and is compatible
        vector_size = len(vector) if hasattr(vector, "__len__") else None
        if vector_size is None:
            raise ValueError("Embedding vector does not provide length; cannot infer dimension")

        # Perform search
        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=k,
            with_payload=True,
        )

        documents: list[Document] = []
        for scored in results:
            payload = getattr(scored, "payload", {}) or {}
            text = payload.get("text", "")
            documents.append(Document(page_content=text, metadata={"score": getattr(scored, "score", None)}))
        return documents
    
    def create_collection(self, collection_name: str, vector_size: int):
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
    
    def add_vectors(self, collection_name: str, vectors_with_docs: list[tuple[Any, Document]]):
        """vectors_with_docs = [(vector, doc), ...]"""
        if not vectors_with_docs:
            return

        # Ensure collection exists and has correct vector size based on first vector
        first_vector = vectors_with_docs[0][0]
        vector_size = len(first_vector) if hasattr(first_vector, "__len__") else None
        if vector_size is None:
            raise ValueError("Embedding vector does not provide length; cannot infer dimension")

        # self._ensure_collection(vector_size)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": doc.page_content}
            )
            for vector, doc in vectors_with_docs
        ]

        try:
            self.client.upsert(collection_name=collection_name, points=points)
        except Exception as e:
            self._logger.error("Upsert failed for collection '%s': %s", collection_name, e)
            raise
    
    def collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name)

    def get_collections_list(self) -> types.CollectionsResponse:
        return self.client.get_collections()