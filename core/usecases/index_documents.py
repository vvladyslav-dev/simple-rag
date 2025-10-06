from core.ports.document_loader import DocumentLoader
from core.ports.embedding_repository import EmbeddingRepository
from core.ports.vector_repository import VectorRepository
from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide
from core.container import Container
from dataclasses import dataclass
from core.ports.usecase import UseCase


@dataclass
class IndexPDFUseCaseResponse:
    success: bool

@dataclass
class IndexPDFUseCaseRequest(GenericQuery[IndexPDFUseCaseResponse]):
    loader: DocumentLoader
    collection_name: str

@Mediator.handler
class IndexPDFUseCase(UseCase[IndexPDFUseCaseRequest, IndexPDFUseCaseResponse]):
    @inject
    def __init__(self,
        vector_repo: VectorRepository = Provide[Container.vector_repository],
        embedder: EmbeddingRepository = Provide[Container.embedding],
    ):
        self.vector_repo = vector_repo
        self.embedder = embedder

    def handle(self, request: IndexPDFUseCaseRequest) -> IndexPDFUseCaseResponse:
        docs = request.loader.load()
        
        vectors = []
        for doc in docs:
            vector = self.embedder.embed(doc.page_content)
            vectors.append((vector, doc)) 
        
        self.vector_repo.create_collection(request.collection_name, len(vectors[0][0]))
        self.vector_repo.add_vectors(request.collection_name, vectors)
        return IndexPDFUseCaseResponse(success=True)