"""
API module for communicating with the RAG backend service.
Handles all HTTP requests to the FastAPI backend endpoints.
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from typing import Dict, Any

import requests  # HTTP client library for making API calls

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from .config import api_base_url  # Backend URL configuration

# =============================================================================
# API FUNCTION: QUERY
# =============================================================================

def api_query(query: str, user_id: str = "", file_name: str = "") -> Dict[str, Any]:
    """
    Send a query to the RAG backend and get a response.

    This function calls the POST /query endpoint with the user's question.
    Optionally includes user_id and file_name if a document has been uploaded.

    Args:
        query (str): The user's question/query text.
        user_id (str, optional): Unique identifier from file upload.
            Defaults to empty string. Include this when a document is uploaded.
        file_name (str, optional): Name of the uploaded file.
            Defaults to empty string. Helps backend locate the relevant context.

    Returns:
        Dict[str, Any]: JSON response containing:
            - "response": The generated answer text
            - "images": List of base64-encoded image strings

    Raises:
        requests.HTTPError: If the API call fails (non-2xx status code).
    """
    # Construct the full API endpoint URL by combining base URL with path
    endpoint = f"{api_base_url}/query"

    # Prepare the JSON payload with query data
    # question: The actual text query from the user
    # user_id: Tracks which user's context to use (from file upload)
    # file_name: Helps backend retrieve relevant document chunks
    payload = {
        "question": query,
        "user_id": user_id,
        "file_name": file_name
    }

    # Make POST request to the backend API
    # json= payload sends the data as JSON in the request body
    response = requests.post(endpoint, json=payload)

    # Raise an exception for HTTP error status codes (4xx, 5xx)
    # This helps us catch and handle API errors gracefully
    response.raise_for_status()

    # Parse and return the JSON response as a Python dictionary
    return response.json()

# =============================================================================
# API FUNCTION: UPLOAD
# =============================================================================

def api_upload(file) -> str:
    """
    Upload a file to the RAG backend for processing.

    This function sends the PDF file to the POST /upload endpoint.
    The backend processes the file, creates embeddings, and returns a user_id
    that can be used to query the document later.

    Args:
        file: File object from Streamlit's file_uploader widget.
            Should be a PDF file.

    Returns:
        str: User ID string returned by the backend.
            This ID is required for subsequent query requests.

    Raises:
        requests.HTTPError: If the API call fails (non-2xx status code).
    """
    # Construct the full API endpoint URL
    endpoint = f"{api_base_url}/upload"

    # Prepare the file for upload
    # files parameter expects a dictionary with:
    #   - key: field name ("file" must match backend's expected parameter name)
    #   - value: tuple of (filename, file_object, MIME_type)
    # The MIME type helps the backend properly handle the file
    files = {
        "file": (file.name, file, file.type)
    }

    # Make POST request with multipart/form-data encoding
    # The requests library automatically handles the file encoding
    response = requests.post(endpoint, files=files)

    # Check for HTTP errors
    response.raise_for_status()

    # Extract the user_id from the JSON response
    # The backend returns {"user_id": "..."} after successful upload
    return response.json()['user_id']