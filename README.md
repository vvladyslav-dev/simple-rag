## RAG App (Streamlit + Qdrant + Gemini)

Interactive RAG application: upload PDF files, index them into a vector database, choose a collection (context), and ask questions. Uses Google Gemini models for both generation and embeddings. Thanks to a clean architecture, you can easily swap LLMs, embeddings, or the vector store.

### Features
- Upload PDF documents and split them into chunks
- Index chunks into Qdrant (vector database)
- List existing collections and select the context before querying
- Generate answers grounded in the selected collection
- Gemini models: `gemini-2.5-flash` (LLM) and `gemini-embedding-001` (embeddings)
- Clean architecture (ports/adapters, DI) — easy to replace models and/or storage

### Requirements
- Python 3.11
- Google Generative AI API key (`GOOGLE_API_KEY`)
- Optional: `QDRANT_URL` if you don’t use Docker Compose (defaults to `http://qdrant:6333`)

### Environment variables (.env)
Place a minimal `.env` at the project root:
```
GOOGLE_API_KEY=your_google_api_key
# QDRANT_URL=http://localhost:6333  # optional if Qdrant is not in Docker
```

### Run locally
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
App will be available at `http://localhost:8501`.

### Run with Docker Compose
```bash
docker compose up -d
```
This starts:
- Qdrant on ports `6333/6334` (data persisted in `qdrant_data/`)
- Streamlit at `http://localhost:8501`

Ensure `.env` with `GOOGLE_API_KEY` exists at the project root before starting.

### How to use
1. Upload a PDF — a collection named after the file will be created (or updated).
2. Choose a collection from the list (your RAG context).
3. Ask a question — the answer will be generated using the selected collection.
4. To index multiple documents, upload them one by one (each becomes its own collection) and switch context via the selector.

### Architecture and extensibility
- Ports: `core/ports` (`LLMRepository`, `EmbeddingRepository`, `VectorRepository`)
- Implementations: `infrastructure/llm`, `infrastructure/embedding`, `infrastructure/vector_db`
- DI container: `core/container.py`

To replace models or storage, implement the port interface and wire it in the container — no other code changes needed.

### Tech stack
- Streamlit — UI
- Qdrant — vector database
- Google Gemini — LLM and embeddings (via `langchain_google_genai`)
- LangChain — integrations and utilities
