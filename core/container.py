from dependency_injector import containers, providers
from infrastructure.embedding.gemeni_embedding import GeminiEmbedding
from infrastructure.llm.gemeni_llm import GeminiLLM
from infrastructure.vector_db.qdrant_repository import QdrantRepository
from infrastructure.document_loaders.pdf_loader import PDFDocumentLoader

class Container(containers.DeclarativeContainer):
    embedding = providers.Singleton(GeminiEmbedding)
    vector_repository = providers.Singleton(QdrantRepository)
    llm = providers.Singleton(GeminiLLM)

    pdf_loader = providers.Factory(PDFDocumentLoader)
