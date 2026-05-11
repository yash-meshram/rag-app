import base64
import io
from PIL import Image
import streamlit as st
from app import api
from app import state
from app.config import (
    ALLOWED_FILE_TYPES,
    STATUS_IDLE,
    STATUS_UPLOADING,
    STATUS_DONE
)


def display_chat_history() -> None:
    chat_history = state.get_chat_history()

    for message in chat_history:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
                for image_base64 in message.get("images", []):
                    display_base64_image(image_base64)


def render_file_upload_sidebar() -> None:
    st.sidebar.title("📄 Document Upload")

    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",
        type=ALLOWED_FILE_TYPES
    )

    if uploaded_file and st.session_state[state.UPLOAD_STATUS_KEY] == STATUS_IDLE:
        st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_UPLOADING
        st.session_state[state.FILE_NAME_KEY] = str(uploaded_file.name)

        with st.sidebar:
            with st.spinner("⏳ Uploading file..."):
                user_id = api.api_upload(file=uploaded_file)

                if user_id:
                    st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_DONE
                    st.session_state[state.USER_ID_KEY] = user_id
                    st.success("✅ File uploaded successfully!")
                else:
                    st.session_state[state.UPLOAD_STATUS_KEY] = STATUS_IDLE
                    st.error("❌ Failed to upload file.")

    if st.session_state[state.UPLOAD_STATUS_KEY] == STATUS_DONE:
        file_name = st.session_state.get(state.FILE_NAME_KEY, "")
        st.sidebar.info(f"📎 Current file: **{file_name}**")

    st.sidebar.divider()
    if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
        state.clear_chat_history()
        st.rerun()


def handle_chat_submit(user_query: str) -> None:
    state.add_user_message(user_query)

    with st.chat_message("user", avatar="👤"):
        st.write(user_query)

    upload_status = st.session_state.get(state.UPLOAD_STATUS_KEY)
    user_id = st.session_state.get(state.USER_ID_KEY, "")
    file_name = st.session_state.get(state.FILE_NAME_KEY, "")

    api_params = {"query": user_query}

    if upload_status == STATUS_DONE and user_id:
        api_params["user_id"] = user_id
        api_params["file_name"] = file_name

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = api.api_query(**api_params)
                
                st.write(response["response"])
                
                images = response.get("images", [])
                
                for image_base64 in images:
                    display_base64_image(image_base64)

                state.add_assistant_message(response["response"], images)

            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                state.add_assistant_message(error_message, [])


def display_base64_image(image_b64_string: str) -> None:
    image_bytes = base64.b64decode(image_b64_string)
    image_stream = io.BytesIO(image_bytes)
    image = Image.open(image_stream)

    st.image(image, width="stretch")


def render_app() -> None:
    state.initialize_session_state()

    st.title("💬 RAG Chat")

    render_file_upload_sidebar()

    display_chat_history()

    if user_query := st.chat_input("Ask a question..."):
        handle_chat_submit(user_query)