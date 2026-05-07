# Web Frontend (`web`)

Streamlit UI for:

- Uploading a PDF to the backend
- Sending user questions to the RAG API
- Rendering generated answers and returned base64 images

## Entry Point

- `streamlit_app.py`

## Environment Variable

Set in `.env` (project root):

```env
API_BASE_URL=http://localhost:8000
```

If not set, the app defaults to `http://localhost:8000`.

## Run Frontend

From project root:

```bash
streamlit run web/streamlit_app.py
```

## How It Works

- Select a PDF in the sidebar upload widget.
- The app calls `POST /upload` and stores `user_id` and `file_name` in Streamlit session state.
- Enter a query in the text field.
- The app calls `POST /query` with the current context and renders:
  - `response` text
  - any returned images (decoded from base64)
