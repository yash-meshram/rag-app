"""
RAG Streamlit Application - Web Frontend Package

This package contains the modular structure for the RAG (Retrieval-Augmented Generation)
application frontend built with Streamlit.

Modules:
    - config: Application configuration and constants
    - api: Backend API communication functions
    - state: Session state management
    - ui: User interface rendering components

For more information, see the README.md in the web directory.
"""

# Import the main render function for easy access from streamlit_app.py
from .ui import render_app

# Define package version
__version__ = "1.0.0"