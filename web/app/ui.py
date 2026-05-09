"""
User Interface (UI) module for the RAG Streamlit application.
Contains all UI rendering functions for file upload, chat, and image display.
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import base64  # For decoding base64-encoded image strings
import io      # For converting bytes to image in memory

from PIL import Image  # Python Imaging Library for image handling

import streamlit as st  # Streamlit library for web UI

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
from . import api  # API functions for backend communication
from . import state  # Session state management functions
from .config import (
    ALLOWED_FILE_TYPES,  # List of allowed file extensions
    CHAT_HISTORY_KEY,    # Key for chat history in session state
    STATUS_IDLE,         # Upload status: idle
    STATUS_UPLOADING,     # Upload status: uploading
    STATUS_DONE,          # Upload status: done
)

# =============================================================================
# UI FUNCTION: DISPLAY CHAT HISTORY
# =============================================================================

def display_chat_history() -> None:
    """
    Display the entire chat history in the main content area.

    This function iterates through all messages in the chat history
    and renders them with appropriate styling. User messages appear
    on the right with blue background, assistant messages on the left
    with gray background.
    """
    # Get the chat history from session state
    chat_history = state.get_chat_history()

    # Iterate through each message in the history
    for message in chat_history:
        # Check if this is a user message or assistant message
        if message["role"] == "user":
            # Render user message with blue background, aligned right
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            # Render assistant message with gray background, aligned left
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
                # Display any images associated with this response
                for image_base64 in message.get("images", []):
                    display_base64_image(image_base64)

# =============================================================================
# UI FUNCTION: FILE UPLOAD SIDEBAR
# =============================================================================

def render_file_upload_sidebar() -> None:
    """
    Render the file upload widget in the Streamlit sidebar.

    This function creates a file upload section in the sidebar where
    users can select and upload PDF documents. When a file is uploaded,
    it calls the backend API and stores the returned user_id for later use.

    Flow:
    1. Display upload widget
    2. If file selected and no upload in progress, start upload
    3. Show spinner during upload
    4. On success, update session state with user_id
    5. On failure, show error message
    """
    # Set the sidebar title
    st.sidebar.title("📄 Document Upload")

    # Create file uploader widget in sidebar
    # type parameter restricts selectable files to PDFs
    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",  # Label text shown to user
        type=ALLOWED_FILE_TYPES  # ["pdf"] - only allow PDF files
    )

    # Check if file is uploaded AND upload hasn't started yet
    # This prevents duplicate uploads when the page reruns
    if uploaded_file and st.session_state[state.UPLOAD_STATUS_KEY] == STATUS_IDLE:
        # Mark upload as in progress
        st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_UPLOADING

        # Store the file name in session state
        st.session_state[state.FILE_NAME_KEY] = str(uploaded_file.name)

        # Create a container in the sidebar for the spinner
        with st.sidebar:
            # Show spinner with message while uploading
            with st.spinner("⏳ Uploading file..."):
                # Call the upload API function
                user_id = api.api_upload(file=uploaded_file)

                # Check if upload was successful
                if user_id:
                    # Update state to indicate upload is complete
                    st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_DONE
                    st.session_state[state.USER_ID_KEY] = user_id
                    st.success("✅ File uploaded successfully!")
                else:
                    # Reset state on failure
                    st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_IDLE
                    st.error("❌ Failed to upload file.")

    # Display current file info if a file has been uploaded
    if st.session_state[state.UPLOAD_STATUS_KEY] == STATUS_DONE:
        file_name = st.session_state.get(state.FILE_NAME_KEY, "")
        st.sidebar.info(f"📎 Current file: **{file_name}**")

    # Add clear chat button to sidebar
    st.sidebar.divider()
    if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
        state.clear_chat_history()
        st.rerun()

# =============================================================================
# UI FUNCTION: HANDLE CHAT SUBMISSION
# =============================================================================

def handle_chat_submit(user_query: str) -> None:
    """
    Handle the submission of a chat message.

    This function processes the user's query:
    1. Adds the user's message to chat history
    2. Calls the API to get a response
    3. Adds the assistant's response to chat history

    Args:
        user_query (str): The text query entered by the user.
    """
    # Add the user's message to chat history
    state.add_user_message(user_query)

    # Display user message immediately
    with st.chat_message("user", avatar="👤"):
        st.write(user_query)

    # Determine if we have document context (file uploaded)
    upload_status = st.session_state.get(state.UPLOAD_STATUS_KEY)
    user_id = st.session_state.get(state.USER_ID_KEY, "")
    file_name = st.session_state.get(state.FILE_NAME_KEY, "")

    # Prepare API call parameters
    api_params = {"query": user_query}

    # Include document context if file was uploaded
    if upload_status == STATUS_DONE and user_id:
        api_params["user_id"] = user_id
        api_params["file_name"] = file_name

    # Call the API and get response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Make the API call
                response = api.api_query(**api_params)

                # Display the response text
                st.write(response["response"])

                # Display any images returned by the API
                images = response.get("images", [])
                for image_base64 in images:
                    display_base64_image(image_base64)

                # Add assistant's response to chat history
                state.add_assistant_message(response["response"], images)

            except Exception as e:
                # Handle API errors gracefully
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                # Add error to chat history as well
                state.add_assistant_message(error_message, [])

# =============================================================================
# UI FUNCTION: DISPLAY IMAGE
# =============================================================================

def display_base64_image(image_b64_string: str) -> None:
    """
    Display an image from a base64-encoded string.

    This function takes a base64-encoded image string (commonly returned
    by AI models when generating images), decodes it, converts it to a
    PIL Image object, and renders it in the Streamlit interface.

    Args:
        image_b64_string (str): Base64-encoded image data.
            Typically starts with data type prefix like "data:image/png;base64,..."
            or could be raw base64 without prefix.
    """
    # Decode the base64 string to raw bytes
    # b64decode expects raw base64 without the data URI prefix
    image_bytes = base64.b64decode(image_b64_string)

    # Create an in-memory binary stream from the image bytes
    # PIL's Image.open() can read from file-like objects
    image_stream = io.BytesIO(image_bytes)

    # Open the image using PIL
    # Image.open() doesn't load the image data immediately,
    # it just identifies the format and prepares for reading
    image = Image.open(image_stream)

    # Render the image in the Streamlit interface
    # use_column_width=True makes the image span the full column width
    st.image(image, use_column_width=True)

# =============================================================================
# UI FUNCTION: HANDLE PENDING QUERY
# =============================================================================

def execute_pending_query() -> None:
    """
    Execute any pending query after file upload completes.

    This function is called during page reruns after a file upload.
    It checks if there's a pending query stored in session state
    and executes it with the user_id and file_name from the upload.

    After execution, the pending query is cleared from session state.
    """
    # Check if conditions are met:
    # 1. File upload is complete (status = "done")
    # 2. There is a pending query waiting to be executed
    if (st.session_state[state.UPLOAD_STATUS_KEY] == STATUS_DONE and
            st.session_state[state.PENDING_QUERY_KEY] is not None):

        # Retrieve the stored query and file info
        query = st.session_state[state.PENDING_QUERY_KEY]
        user_id = st.session_state[state.USER_ID_KEY]
        file_name = st.session_state[state.FILE_NAME_KEY]

        # Call the API with the query and document context
        response = api.api_query(
            query=query,
            user_id=user_id,
            file_name=file_name
        )

        # Display the text response from the backend
        st.write(response["response"])

        # Check if the response includes any images
        # The backend can return multiple images in the "images" list
        for image_base64_str in response["images"]:
            # Render each returned image in the UI
            display_base64_image(image_base64_str)

        # Clear the pending query after successful execution
        st.session_state[state.PENDING_QUERY_KEY] = None

# =============================================================================
# MAIN RENDER FUNCTION
# =============================================================================

def render_app() -> None:
    """
    Main function to render all UI components in the correct order.

    This function orchestrates the UI rendering sequence:
    1. Initialize session state variables
    2. Render chat history (existing messages)
    3. Render chat input (for new messages)
    4. Render file upload sidebar
    """
    # Step 1: Ensure all session state variables are initialized
    state.initialize_session_state()

    # Step 2: Display the header
    st.title("💬 RAG Chat")

    # Step 3: Render file upload widget in sidebar
    render_file_upload_sidebar()

    # Step 4: Display any existing chat history
    display_chat_history()

    # Step 5: Create chat input and handle submissions
    # st.chat_input creates a text input at the bottom of the page
    if user_query := st.chat_input("Ask a question..."):
        handle_chat_submit(user_query)