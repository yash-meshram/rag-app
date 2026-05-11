# RAG Backend (`rag`)

FastAPI backend for document ingestion and retrieval-augmented generation.

## What It Does

- Accepts PDF uploads
- Extracts text and images from documents
- Generates image descriptions using the configured LLM
- Chunks content and stores embeddings in MongoDB Atlas Vector Search
- Runs hybrid retrieval + reranking for grounded answering

## Source Layout

- `main.py` - FastAPI app bootstrap and router registration
- `app/routes/upload.py` - `POST /upload`
- `app/routes/query.py` - `POST /query`
- `app/services/` - ingestion, parsing, chunking, retrieval, hybrid search, image handling
- `app/db/mongo.py` - MongoDB Atlas client and vector store setup
- `app/models/llm.py` - LLM singleton (`ChatGroq`)
- `app/schemas/request.py` - request payload models

## Environment Variables

Set these for the backend process (for example in `rag/.env`):

```env
MONGODB_ATLAS_CLUSTER_URI=...
MONGODB_ATLAS_DB=...
MONGODB_ATLAS_COLLECTION=...
VECTOR_SEARCH_INDEX_NAME=...
KEYWORD_SEARCH_INDEX_NAME=...
HUGGINGFACE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
META_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
GROQ_API_KEY=...
```

## Run Backend

From repository root:

```bash
cd rag
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

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

Note: schema currently expects `question`, `user_id`, and `file_name` keys in payload.

- Response with retrieval context:

```json
{
  "response": "answer text",
  "images": ["<base64-image>", "..."]
}
```

- Response without retrieval context:

```json
{
  "response": "answer text"
}
```

## Ingestion and Retrieval Notes

- Upload route writes temporary files under `app/data/` and removes them after ingestion.
- Retrieval flow:
  1. Query enhancement
  2. Hybrid search (vector + keyword)
  3. Cross-encoder reranking
  4. Final answer generation with referenced content
