from mediatr import Mediator, GenericQuery
from core.ports.usecase import UseCase
from core.ports.vector_repository import VectorRepository
from dependency_injector.wiring import inject, Provide
from core.container import Container
from dataclasses import dataclass
from qdrant_client.conversions import common_types as types


@dataclass
class GetCollectionsListUseCaseResponse:
    collections: types.CollectionsResponse

@dataclass
class GetCollectionsListUseCaseRequest(GenericQuery[GetCollectionsListUseCaseResponse]):
    pass

@Mediator.handler
class GetCollectionsListUseCase(UseCase[GetCollectionsListUseCaseRequest, GetCollectionsListUseCaseResponse]):
    @inject
    def __init__(self, repository: VectorRepository = Provide[Container.vector_repository]):
        self._repository = repository
    
    def handle(self, request: GetCollectionsListUseCaseRequest) -> GetCollectionsListUseCaseResponse:
        collections: types.CollectionsResponse = self._repository.get_collections_list()
        return GetCollectionsListUseCaseResponse(collections=collections)