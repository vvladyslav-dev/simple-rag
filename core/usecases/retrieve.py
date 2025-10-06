from dataclasses import dataclass
from langchain_core.documents import Document
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from core.ports.usecase import UseCase
from core.ports.vector_repository import VectorRepository
from core.ports.embedding_repository import EmbeddingRepository
from core.container import Container


@dataclass
class RetrieveUseCaseResponse:
    context: list[Document]


@dataclass
class RetrieveUseCaseRequest(GenericQuery[RetrieveUseCaseResponse]):
    question: str
    collection_name: str


@Mediator.handler
class RetrieveUseCase(UseCase[RetrieveUseCaseRequest, RetrieveUseCaseResponse]):
    @inject
    def __init__(
        self,
        repository: VectorRepository = Provide[Container.vector_repository],
        embedding_repository: EmbeddingRepository = Provide[Container.embedding],
    ):
        self._repository = repository
        self._embedding_repository = embedding_repository

    def handle(self, request: RetrieveUseCaseRequest) -> RetrieveUseCaseResponse:
        query_vector = self._embedding_repository.embed(request.question)
        retrieved_docs = self._repository.similarity_search_by_vector(request.collection_name, query_vector)
        return RetrieveUseCaseResponse(context=retrieved_docs)