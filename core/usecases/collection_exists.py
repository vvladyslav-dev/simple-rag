from mediatr import Mediator, GenericQuery
from core.ports.usecase import UseCase
from core.ports.vector_repository import VectorRepository
from dependency_injector.wiring import inject, Provide
from core.container import Container
from dataclasses import dataclass


@dataclass
class CollectionExistsUseCaseResponse:
    exists: bool


@dataclass
class CollectionExistsUseCaseRequest(GenericQuery[CollectionExistsUseCaseResponse]):
    collection_name: str


@Mediator.handler
class CollectionExistsUseCase(
    UseCase[CollectionExistsUseCaseRequest, CollectionExistsUseCaseResponse]
):
    @inject
    def __init__(
        self, repository: VectorRepository = Provide[Container.vector_repository]
    ):
        self._repository = repository
    
    def handle(self, request: CollectionExistsUseCaseRequest) -> CollectionExistsUseCaseResponse:
        exists: bool = self._repository.collection_exists(request.collection_name)
        return CollectionExistsUseCaseResponse(exists=exists)