import streamlit as st
from app import render_app


st.set_page_config(
    page_title="RAG-app",
    initial_sidebar_state="expanded",
    layout="wide"
)


render_app()