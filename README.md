# rag-app

A Retrieval-Augmented Generation (RAG) app with:

- `rag/`: FastAPI backend for PDF ingestion, hybrid retrieval, reranking, and answer generation
- `web/`: Streamlit frontend for file upload and chat

## Architecture Overview

The app runs as two services:

- **Backend (`rag`)**
  - Entry point: `rag/main.py`
  - Routes: `POST /upload`, `POST /query`
  - Pipeline:
    1. Parse PDF text and images
    2. Generate image descriptions with LLM
    3. Chunk parsed content
    4. Store vectors in MongoDB Atlas Vector Search
    5. Run hybrid search + reranking at query time
    6. Generate final answer with LLM

- **Frontend (`web`)**
  - Entry point: `web/streamlit_app.py`
  - Uploads PDFs to backend and stores `user_id`/`file_name` in session
  - Sends chat queries with or without document context
  - Displays answer text and returned images

## Repository Structure

- `rag/main.py` - FastAPI app bootstrap
- `rag/app/routes/` - API endpoints
- `rag/app/services/` - ingestion, retrieval, chunking, hybrid search, image handling
- `rag/app/db/mongo.py` - MongoDB Atlas + vector store setup
- `rag/app/models/llm.py` - LLM client initialization (`ChatGroq`)
- `rag/app/schemas/` - request schema(s)
- `web/streamlit_app.py` - Streamlit launcher
- `web/app/` - UI, state management, backend API client config
- `requirements.txt` - root Python dependencies

## Poject Architecture
![Architecture Diagram](images/Architecture%20Diagram.png)

## Prerequisites

- Python 3.10+
- MongoDB Atlas cluster
- Atlas indexes:
  - one **vector** search index
  - one **keyword/full-text** search index
- Groq API key with access to your selected model

## Setup

1. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

You can place a `.env` file inside `rag/` (recommended for backend because `rag/main.py` loads dotenv), or export variables in your shell.

Example:

```env
# MongoDB Atlas
MONGODB_ATLAS_CLUSTER_URI=...
MONGODB_ATLAS_DB=...
MONGODB_ATLAS_COLLECTION=...
VECTOR_SEARCH_INDEX_NAME=...
KEYWORD_SEARCH_INDEX_NAME=...

# Embedding + reranker models
HUGGINGFACE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

# LLM
GROQ_API_KEY=...
META_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# Frontend -> backend endpoint
API_BASE_URL=http://localhost:8000
```

## Run the Application

### Terminal 1 - FastAPI backend

From repository root:

```bash
cd rag
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Streamlit frontend

From repository root:

```bash
streamlit run web/streamlit_app.py
```

Open the Streamlit URL shown in terminal (usually `http://localhost:8501`).

## API Contracts

### `POST /upload`

- Request: multipart form-data with `file` (PDF)
- Response:

```json
{
  "user_id": "uuid-string",
  "file_name": "uploaded.pdf"
}
```

### `POST /query`

- Request JSON:

```json
{
  "question": "What is this document about?",
  "user_id": "uuid-string",
  "file_name": "uploaded.pdf"
}
```

- Response (document mode):

```json
{
  "response": "answer text",
  "images": ["<base64-image>", "..."]
}
```

- Response (no file context):

```json
{
  "response": "answer text"
}
```

## Typical User Flow

1. Start backend and frontend.
2. Upload a PDF from sidebar.
3. Receive and store `user_id` + `file_name`.
4. Ask questions in chat.
5. Backend retrieves relevant chunks, reranks, and returns answer + images.

## Sequential Diagram
![Sequential Diagram](images/Sequential%20Diagram.png)

## Troubleshooting

- **`ModuleNotFoundError: No module named 'app'`**  
  Run backend from `rag/` using `uvicorn main:app ...`.

- **Backend connection errors from Streamlit**  
  Ensure backend is running and `API_BASE_URL` points to it.

- **MongoDB search returns empty/low-quality results**  
  Check vector/keyword index names and model env values.

- **`422` on `/query`**  
  The current backend schema expects `question`, `user_id`, and `file_name` keys in payload.

## Security Note

Do not commit real secrets (API keys, DB URIs, tokens) to git. Keep `.env` files local and rotate any leaked credentials.

## Additional Docs

- Backend notes: `rag/README.md`
- Frontend notes: `web/README.md`