# RAG Backend (`rag`)

FastAPI service that handles:

- PDF upload and ingestion
- Chunking and storage in MongoDB Atlas vector search
- Query enhancement, hybrid retrieval, reranking, and LLM response generation

## Main Components

- `main.py` - FastAPI app entrypoint
- `routes/upload.py` - `POST /upload` endpoint
- `routes/query.py` - `POST /query` endpoint
- `services/` - ingestion, retrieval, chunking, hybrid search, and document processing
- `db/mongo.py` - MongoDB Atlas and vector store initialization
- `models/llm.py` - LLM client setup (`ChatGroq`)

## Environment Variables

Set these in project root `.env`:

```env
MONGODB_ATLAS_CLUSTER_URI=...
MONGODB_ATLAS_DB=...
MONGODB_ATLAS_COLLECTION=...
VECTOR_SEARCH_INDEX_NAME=...
KEYWORD_SEARCH_INDEX_NAME=...
META_VISION_MODEL=...
GROQ_API_KEY=...
```

## Run Backend

From project root:

```bash
uvicorn rag.main:app --reload --host 0.0.0.0 --port 8000
```

## API Contract

### `POST /upload`

- Form data:
  - `file`: PDF file
- Response:
  - `user_id`: generated user/session id
  - `file_name`: uploaded file name

### `POST /query`

- JSON body:
  - `question` (string, required)
  - `user_id` (string, optional when querying uploaded docs)
  - `file_name` (string, optional when querying uploaded docs)
- Response:
  - `response`: generated answer text
  - `images` (optional): base64 image list when retrieval returns image chunks

## Notes

- Uploaded PDFs are temporarily written to `rag/data/` during ingestion and deleted afterward.
- Retrieval flow includes query enhancement and reranking before final answer generation.
# RAG Backend (`rag`)

FastAPI service that handles:

- PDF upload and ingestion
- Chunking and storage in MongoDB Atlas vector search
- Query enhancement, hybrid retrieval, reranking, and LLM response generation

## Main Components

- `main.py` - FastAPI app entrypoint
- `routes/upload.py` - `POST /upload` endpoint
- `routes/query.py` - `POST /query` endpoint
- `services/` - ingestion, retrieval, chunking, hybrid search, and document processing
- `db/mongo.py` - MongoDB Atlas and vector store initialization
- `models/llm.py` - LLM client setup (`ChatGroq`)

## Environment Variables

Set these in project root `.env`:

```env
MONGODB_ATLAS_CLUSTER_URI=...
MONGODB_ATLAS_DB=...
MONGODB_ATLAS_COLLECTION=...
VECTOR_SEARCH_INDEX_NAME=...
KEYWORD_SEARCH_INDEX_NAME=...
META_VISION_MODEL=...
GROQ_API_KEY=...
```

## Run Backend

From project root:

```bash
uvicorn rag.main:app --reload --host 0.0.0.0 --port 8000
```

## API Contract

### `POST /upload`

- Form data:
  - `file`: PDF file
- Response:
  - `user_id`: generated user/session id
  - `file_name`: uploaded file name

### `POST /query`

- JSON body:
  - `question` (string, required)
  - `user_id` (string, optional when querying uploaded docs)
  - `file_name` (string, optional when querying uploaded docs)
- Response:
  - `response`: generated answer text
  - `images` (optional): base64 image list when retrieval returns image chunks

## Notes

- Uploaded PDFs are temporarily written to `rag/data/` during ingestion and deleted afterward.
- Retrieval flow includes query enhancement and reranking before final answer generation.
