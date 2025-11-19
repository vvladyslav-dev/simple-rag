from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
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
        # Create RAG prompt template directly instead of using hub
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Use the following pieces of context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer."),
            ("human", "Context: {context}\n\nQuestion: {question}")
        ]) 

    def invoke(self, messages: str) -> str:
        response: Any = self.model.invoke(messages)
        return getattr(response, "content", str(response))
    
    def generate_answer(self, question: str, context: str) -> str:
        messages = self.prompt.invoke({"question": question, "context": context})
        response = self.model.invoke(messages)
        return getattr(response, "content", str(response))