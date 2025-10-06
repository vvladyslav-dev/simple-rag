from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain import hub
from typing import Any

from core.ports.llm_repository import LLMRepository

load_dotenv()

class GeminiLLM(LLMRepository):
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.prompt = hub.pull("rlm/rag-prompt") 

    def invoke(self, messages: str) -> str:
        response: Any = self.model.invoke(messages)
        return getattr(response, "content", str(response))
    
    def generate_answer(self, question: str, context: str) -> str:
        messages = self.prompt.invoke({"question": question, "context": context})
        response = self.model.invoke(messages)
        return getattr(response, "content", str(response))