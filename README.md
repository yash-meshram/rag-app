# rag-app

A simple Retrieval-Augmented Generation (RAG) application with:

- `rag`: FastAPI backend for document upload, ingestion, retrieval, and response generation
- `web`: Streamlit frontend for uploading PDFs and chatting with your data

## Project Structure

- `rag/` - backend API and RAG pipeline
- `web/` - Streamlit client UI
- `requirements.txt` - Python dependencies for both backend and frontend
- `.env` - environment variables (not committed)

## Prerequisites

- Python 3.10+
- A MongoDB Atlas cluster with vector and keyword search indexes
- A Groq API key and model access (used through `langchain_groq`)

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure `.env` in the project root with required values:

```env
MONGODB_ATLAS_CLUSTER_URI=...
MONGODB_ATLAS_DB=...
MONGODB_ATLAS_COLLECTION=...
VECTOR_SEARCH_INDEX_NAME=...
KEYWORD_SEARCH_INDEX_NAME=...
META_VISION_MODEL=...
GROQ_API_KEY=...
API_BASE_URL=http://localhost:8000
```

## Run the App

Start backend (terminal 1):

```bash
uvicorn rag.main:app --reload --host 0.0.0.0 --port 8000
```

Start frontend (terminal 2):

```bash
streamlit run web/streamlit_app.py
```

Then open the Streamlit URL shown in terminal (usually `http://localhost:8501`).

## API Endpoints

- `POST /upload` - upload a PDF and ingest document chunks
- `POST /query` - ask questions globally or against uploaded document context

## More Docs

- Backend details: `rag/README.md`
- Frontend details: `web/README.md`