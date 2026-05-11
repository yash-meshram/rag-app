import os

api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

UPLOAD_STATUS_KEY = "file_upload_status"

FILE_NAME_KEY = "file_name"

USER_ID_KEY = "user_id"

CHAT_HISTORY_KEY = "chat_history"

PENDING_QUERY_KEY = "pending_query"

STATUS_IDLE = "idle"
STATUS_UPLOADING = "uploading"
STATUS_DONE = "done"

ALLOWED_FILE_TYPES = ["pdf"]

PDF_MIME_TYPE = "application/pdf"