from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.ports.document_loader import DocumentLoader
from typing import Any

class PDFDocumentLoader(DocumentLoader):
    def __init__(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load(self) -> list[Any]:
        loader = PyPDFLoader(self.file_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        return chunks
