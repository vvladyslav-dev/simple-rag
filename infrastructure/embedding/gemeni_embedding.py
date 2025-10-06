from core.ports.embedding_repository import EmbeddingRepository
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import Any

class GeminiEmbedding(EmbeddingRepository):
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
    def embed(self, text: str) -> Any:
        return self.embeddings.embed_query(text)