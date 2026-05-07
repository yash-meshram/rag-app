import streamlit as st
import os
import requests
import base64
from PIL import Image
import io
# from fastapi import UploadFile

# Helper
api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

def api_query(query: str, user_id: str = "", file_name: str = ""):
    response: dict = requests.post(
        f"{api_base_url}/query",
        json = {
            "question": query,
            "user_id": user_id,
            "file_name": file_name
        }
    )
    response.raise_for_status()
    return response.json()

def api_upload(file):
    response: dict = requests.post(
        f"{api_base_url}/upload",
        files={
            "file": (file.name, file, file.type)
        }
    )
    response.raise_for_status()
    return response.json()['user_id']

# Page config
st.set_page_config(
    page_title = "RAG-app",
    initial_sidebar_state = "expanded",
    layout = "wide"
)


# Sidebar for file upload
st.sidebar.title("+ Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# file uploaded
if "file_upload_status" not in st.session_state:
    st.session_state.file_upload_status = "idle"
if "file_name" not in st.session_state:
    st.session_state.file_name = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
    
if uploaded_file and st.session_state.file_upload_status == "idle":
    st.session_state.file_upload_status = "uploading"
    st.session_state.file_name = str(uploaded_file.name)
    
    with st.sidebar:
        with st.spinner("Uploading file"):
            user_id = api_upload(file = uploaded_file)
        
            if user_id:
                st.session_state.file_upload_status = "done"
                st.session_state.user_id = user_id
            else:
                st.session_state.file_upload_status = "idle"
                st.error("Failed to upload file.")


# pending calls
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# chat input
user_query = st.text_input("Type your query...")

if user_query:
    if st.session_state.file_upload_status == "idle" :
        response = api_query(query = user_query)
        st.write(response["response"])        
    else:
        st.session_state.pending_query = user_query
        
# display image
def display_base64_image(image_b64_string):
    # Decode base64 string
    image_bytes = base64.b64decode(image_b64_string)
    
    # Convert to image
    image = Image.open(io.BytesIO(image_bytes))
    
    st.image(image, use_column_width = True)
        
# excuting pending call
if st.session_state.file_upload_status == "done" and st.session_state.pending_query is not None:
    query = st.session_state.pending_query
    user_id = st.session_state.user_id
    file_name = st.session_state.file_name
    response = api_query(
        query = query,
        user_id = user_id,
        file_name = file_name
    )
    st.write(response["response"])
    
    for image_base64_str in response["images"]:
        display_base64_image(image_base64_str)
    
    # clear session
    st.session_state.pending_query = None