"""
RAG Streamlit Application - Main Entry Point

This is the main entry point for the Streamlit web application.
It configures the page settings and renders the UI components.

To run this application:
    streamlit run web/streamlit_app.py

For development, you can also run directly from the web directory:
    cd web && streamlit run streamlit_app.py
"""

# =============================================================================
# STANDARD LIBRARY IMPORTS
# =============================================================================
import streamlit as st  # Streamlit library for building web UI

# =============================================================================
# LOCAL IMPORTS
# =============================================================================
# Import the render_app function from our app package
# This function orchestrates all UI component rendering
from app import render_app

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

# Configure the Streamlit page settings
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title="RAG-app",  # Title shown in browser tab/window
    initial_sidebar_state="expanded",  # Sidebar starts expanded
    layout="wide"  # Use wide layout for more horizontal space
)

# =============================================================================
# RENDER THE APPLICATION UI
# =============================================================================

# Call the main render function to display all UI components
# This handles file upload, chat input, and response display
render_app()

# =============================================================================
# NOTES FOR DEVELOPERS
# =============================================================================

# The app flow works as follows:
#
# 1. User opens the app -> render_app() is called
# 2. Session state is initialized (state.py)
# 3. Title "RAG Chat" is displayed
# 4. File upload widget appears in sidebar (ui.py)
# 5. Chat history is displayed (existing messages)
# 6. Chat input appears at the bottom of the page
#
# User interaction flows:
#
# A. Query without document:
#    - User types query in chat input
#    - Message added to chat history as "user"
#    - api.api_query() is called with empty user_id/file_name
#    - Response added to chat history as "assistant"
#
# B. Upload first, then query:
#    - User uploads PDF via sidebar
#    - api.api_upload() is called, returns user_id
#    - User types query in chat input
#    - api.api_query() is called with user_id and file_name
#    - Response and images added to chat history
#
# C. Query first, then upload:
#    - User types query before upload completes
#    - Query is stored as pending_query
#    - User uploads file
#    - After upload completes, pending_query is executed
#    - Response and images added to chat history
#
# Chat History Features:
# - All messages are persisted in session state
# - User can clear chat history via sidebar button
# - Images returned by the API are displayed inline with responses