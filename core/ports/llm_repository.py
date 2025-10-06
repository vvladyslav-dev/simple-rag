from abc import ABC, abstractmethod


class LLMRepository(ABC):
    @abstractmethod
    def invoke(self, messages: str) -> str:
        pass

    @abstractmethod
    def generate_answer(self, question: str, context: str) -> str:
        pass