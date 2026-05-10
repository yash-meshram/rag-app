"""
Session state management module.
Handles initialization and access to Streamlit session state variables.
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
from typing import Optional

import streamlit as st  # Streamlit library for web UI

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from .config import (
    UPLOAD_STATUS_KEY,  # Key for upload status in session state
    FILE_NAME_KEY,      # Key for file name in session state
    USER_ID_KEY,        # Key for user ID in session state
    PENDING_QUERY_KEY,  # Key for pending query in session state
    CHAT_HISTORY_KEY,   # Key for chat history in session state
    STATUS_IDLE,        # Default status value: "idle"
    STATUS_DONE,        # Upload complete status value: "done"
)

# =============================================================================
# STATE INITIALIZATION
# =============================================================================

def initialize_session_state() -> None:
    """
    Initialize all required session state variables if they don't exist.

    This function should be called at the start of the Streamlit app
    to ensure all required state variables are properly initialized.
    Session state persists data across multiple page reruns.

    Note:
        Streamlit automatically reruns the script when user input changes.
        Without proper initialization, accessing undefined keys would cause errors.
    """
    # Check and initialize file upload status
    # Tracks whether a file has been uploaded, is uploading, or is done
    if UPLOAD_STATUS_KEY not in st.session_state:
        st.session_state[UPLOAD_STATUS_KEY] = STATUS_IDLE

    # Check and initialize file name
    # Stores the name of the uploaded file (e.g., "document.pdf")
    if FILE_NAME_KEY not in st.session_state:
        st.session_state[FILE_NAME_KEY] = ""

    # Check and initialize user ID
    # Stores the unique ID returned by backend after file upload
    if USER_ID_KEY not in st.session_state:
        st.session_state[USER_ID_KEY] = ""

    # Check and initialize pending query
    # Stores a query submitted before upload completed (to execute after upload)
    if PENDING_QUERY_KEY not in st.session_state:
        st.session_state[PENDING_QUERY_KEY] = None

    # Check and initialize chat history
    # Stores the conversation history as a list of message dictionaries
    # Each message: {"role": "user" | "assistant", "content": str, "images": list}
    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []

# =============================================================================
# STATE HELPER FUNCTIONS
# =============================================================================

def is_file_uploaded() -> bool:
    """
    Check if a file has been successfully uploaded.

    Returns:
        bool: True if file upload is complete, False otherwise.
    """
    return st.session_state.get(UPLOAD_STATUS_KEY) == STATUS_DONE

def is_upload_in_progress() -> bool:
    """
    Check if a file upload is currently in progress.

    Returns:
        bool: True if upload is in progress, False otherwise.
    """
    return st.session_state.get(UPLOAD_STATUS_KEY) == "uploading"

def has_pending_query() -> bool:
    """
    Check if there's a query waiting to be executed.

    A pending query occurs when the user submits a query before
    the file upload completes. The query is stored and executed
    automatically after the upload finishes.

    Returns:
        bool: True if there's a pending query, False otherwise.
    """
    return st.session_state.get(PENDING_QUERY_KEY) is not None

def get_pending_query() -> Optional[str]:
    """
    Get the pending query text if one exists.

    Returns:
        Optional[str]: The pending query string, or None if no pending query.
    """
    return st.session_state.get(PENDING_QUERY_KEY)

def clear_pending_query() -> None:
    """
    Clear the pending query from session state.
    Called after the pending query has been executed.
    """
    st.session_state[PENDING_QUERY_KEY] = None

def set_upload_status(status: str) -> None:
    """
    Set the file upload status in session state.

    Args:
        status (str): One of STATUS_IDLE, STATUS_UPLOADING, or STATUS_DONE.
    """
    st.session_state[UPLOAD_STATUS_KEY] = status

def set_file_info(file_name: str, user_id: str) -> None:
    """
    Store file information in session state after successful upload.

    Args:
        file_name (str): Name of the uploaded file.
        user_id (str): User ID returned by the backend.
    """
    st.session_state[FILE_NAME_KEY] = file_name
    st.session_state[USER_ID_KEY] = user_id

def get_file_name() -> str:
    """
    Get the name of the currently uploaded file.

    Returns:
        str: The file name, or empty string if no file uploaded.
    """
    return st.session_state.get(FILE_NAME_KEY, "")

def get_user_id() -> str:
    """
    Get the current user ID from session state.

    Returns:
        str: The user ID, or empty string if not set.
    """
    return st.session_state.get(USER_ID_KEY, "")

# =============================================================================
# CHAT HISTORY HELPER FUNCTIONS
# =============================================================================

def add_user_message(content: str) -> None:
    """
    Add a user message to the chat history.

    Args:
        content (str): The text content of the user's message.
    """
    # Create message dictionary with "user" role
    message = {
        "role": "user",
        "content": content,
        "images": []  # User messages don't have images
    }
    # Append to chat history list
    st.session_state[CHAT_HISTORY_KEY].append(message)

def add_assistant_message(content: str, images: list = None) -> None:
    """
    Add an assistant (AI) message to the chat history.

    Args:
        content (str): The text content of the assistant's response.
        images (list, optional): List of base64-encoded images. Defaults to empty list.
    """
    # Default to empty list if images is None
    if images is None:
        images = []
    # Create message dictionary with "assistant" role
    message = {
        "role": "assistant",
        "content": content,
        "images": images
    }
    # Append to chat history list
    st.session_state[CHAT_HISTORY_KEY].append(message)

def get_chat_history() -> list:
    """
    Get the entire chat history.

    Returns:
        list: List of message dictionaries.
    """
    return st.session_state.get(CHAT_HISTORY_KEY, [])

def clear_chat_history() -> None:
    """
    Clear all messages from the chat history.
    Called when user wants to start a new conversation.
    """
    st.session_state[CHAT_HISTORY_KEY] = []