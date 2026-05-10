"""
Configuration module for the RAG Streamlit application.
Contains API settings, session state keys, and application constants.
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import os  # For reading environment variables

# =============================================================================
# API CONFIGURATION
# =============================================================================
# Base URL for the backend API.
# Priority: 1. Environment variable "API_BASE_URL", 2. Default localhost:8000
# This allows the frontend to communicate with the backend service.
api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

# =============================================================================
# SESSION STATE KEYS
# =============================================================================
# Session state keys are used to store persistent data across Streamlit reruns.
# These keys track the state of file uploads, chat interactions, etc.

# Tracks the current status of file upload process.
# Values: "idle" (no upload), "uploading" (in progress), "done" (completed)
UPLOAD_STATUS_KEY = "file_upload_status"

# Stores the name of the currently uploaded file (e.g., "document.pdf")
FILE_NAME_KEY = "file_name"

# Stores the unique user ID returned by the backend after file upload.
# This ID is required when making subsequent query requests.
USER_ID_KEY = "user_id"

# Stores the chat history as a list of message dictionaries.
# Each message has format: {"role": "user" | "assistant", "content": str, "images": list}
CHAT_HISTORY_KEY = "chat_history"

# Stores a query that was submitted before the file upload completed.
# Once upload finishes, this pending query will be executed automatically.
PENDING_QUERY_KEY = "pending_query"

# =============================================================================
# UPLOAD STATUS VALUES
# =============================================================================
# Possible states for the file upload status tracked in session state.
# These constants make the code more readable and prevent typos.

STATUS_IDLE = "idle"        # No file has been uploaded yet
STATUS_UPLOADING = "uploading"  # File upload is currently in progress
STATUS_DONE = "done"        # File upload completed successfully

# =============================================================================
# FILE CONSTANTS
# =============================================================================
# Allowed file types for upload. Currently only PDF files are supported.
# This list is passed to Streamlit's file_uploader widget.
ALLOWED_FILE_TYPES = ["pdf"]

# MIME type for PDF files. Used when preparing the file for upload.
PDF_MIME_TYPE = "application/pdf"