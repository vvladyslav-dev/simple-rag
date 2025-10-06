from dataclasses import dataclass
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from typing import Any

from core.ports.usecase import UseCase
from core.ports.llm_repository import LLMRepository
from core.container import Container
from langchain_core.documents import Document


@dataclass
class GenerateUseCaseResponse:
    answer: str


@dataclass
class GenerateUseCaseRequest(GenericQuery[GenerateUseCaseResponse]):
    question: str
    context: list[Document]


@Mediator.handler
class GenerateUseCase(UseCase[GenerateUseCaseRequest, GenerateUseCaseResponse]):
    @inject
    def __init__(self, llm: LLMRepository = Provide[Container.llm]):
        self._llm = llm
        self._prompt = getattr(llm, "prompt", None)

    def handle(self, request: GenerateUseCaseRequest) -> GenerateUseCaseResponse:
        docs_content = "\n\n".join(doc.page_content for doc in request.context)
        if self._prompt is None:
            raise ValueError("LLM implementation must provide a 'prompt' attribute")
        messages: Any = self._prompt.invoke({"question": request.question, "context": docs_content})
        response: str = self._llm.invoke(messages)
        return GenerateUseCaseResponse(answer=response)
