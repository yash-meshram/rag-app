# Web Frontend (`web`)

Streamlit UI for the RAG (Retrieval-Augmented Generation) application.

## Features

- Upload PDF documents to the backend for processing
- Query the RAG system with questions
- View generated text responses
- Display AI-generated images (base64 format)

## Project Structure

```
web/
├── app/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration (API URL, constants)
│   ├── api.py            # Backend API functions
│   ├── state.py          # Session state management
│   └── ui.py             # UI component rendering
├── streamlit_app.py      # Main entry point
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Modules Explained

### config.py
Contains application configuration:
- `api_base_url`: Backend API URL (default: http://localhost:8000)
- Session state keys for tracking upload status, user ID, etc.
- Constants for file types and status values

### api.py
Handles HTTP communication with the backend:
- `api_query()`: POST to /query endpoint with question and context
- `api_upload()`: POST to /upload endpoint with PDF file

### state.py
Manages Streamlit session state:
- `initialize_session_state()`: Set up required variables
- Helper functions for checking/modifying state values

### ui.py
Renders all UI components:
- `display_chat_history()`: Renders all previous messages
- `render_file_upload_sidebar()`: PDF upload widget
- `handle_chat_submit()`: Processes user queries and updates history
- `display_base64_image()`: Image rendering

## Environment Variables

Set in `.env` (project root):

```env
API_BASE_URL=http://localhost:8000
```

If not set, defaults to `http://localhost:8000`.

## Installation

```bash
# Install dependencies
pip install -r web/requirements.txt

# Or install individually
pip install streamlit requests Pillow
```

## Running the App

From project root:

```bash
streamlit run web/streamlit_app.py
```

Or from the web directory:

```bash
cd web
streamlit run streamlit_app.py
```

## How It Works

### Flow 1: Query Without Document
1. User types query in text field
2. App calls `POST /query` with `user_id=""` and `file_name=""`
3. Backend returns generic response
4. Response text is displayed

### Flow 2: Upload Then Query
1. User uploads PDF via sidebar
2. App calls `POST /upload` with file
3. Backend returns `user_id`
4. User types query
5. App calls `POST /query` with `user_id` and `file_name`
6. Backend returns contextual response + images
7. Response text and images are displayed

### Flow 3: Query Before Upload Completes
1. User types query (file upload pending)
2. Query is stored as `pending_query`
3. User uploads PDF
4. After upload completes, pending query is executed
5. Response is displayed

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.28.0 | Web UI framework |
| requests | >=2.31.0 | HTTP client for API calls |
| Pillow | >=10.0.0 | Image handling |