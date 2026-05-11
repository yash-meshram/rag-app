from typing import Optional
import streamlit as st


from .config import (
    UPLOAD_STATUS_KEY,
    FILE_NAME_KEY,
    USER_ID_KEY,
    PENDING_QUERY_KEY,
    CHAT_HISTORY_KEY,
    STATUS_IDLE,
    STATUS_DONE
)


def initialize_session_state() -> None:
    if UPLOAD_STATUS_KEY not in st.session_state:
        st.session_state[UPLOAD_STATUS_KEY] = STATUS_IDLE

    if FILE_NAME_KEY not in st.session_state:
        st.session_state[FILE_NAME_KEY] = ""

    if USER_ID_KEY not in st.session_state:
        st.session_state[USER_ID_KEY] = ""

    if PENDING_QUERY_KEY not in st.session_state:
        st.session_state[PENDING_QUERY_KEY] = None

    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []


def is_file_uploaded() -> bool:
    return st.session_state.get(UPLOAD_STATUS_KEY) == STATUS_DONE


def is_upload_in_progress() -> bool:
    return st.session_state.get(UPLOAD_STATUS_KEY) == "uploading"


def has_pending_query() -> bool:
    return st.session_state.get(PENDING_QUERY_KEY) is not None


def get_pending_query() -> Optional[str]:
    return st.session_state.get(PENDING_QUERY_KEY)


def clear_pending_query() -> None:
    st.session_state[PENDING_QUERY_KEY] = None


def set_upload_status(status: str) -> None:
    st.session_state[UPLOAD_STATUS_KEY] = status


def set_file_info(file_name: str, user_id: str) -> None:
    st.session_state[FILE_NAME_KEY] = file_name
    st.session_state[USER_ID_KEY] = user_id


def get_file_name() -> str:
    return st.session_state.get(FILE_NAME_KEY, "")


def get_user_id() -> str:
    return st.session_state.get(USER_ID_KEY, "")


def add_user_message(content: str) -> None:
    message = {
        "role": "user",
        "content": content,
        "images": []
    }
    st.session_state[CHAT_HISTORY_KEY].append(message)


def add_assistant_message(content: str, images: list = None) -> None:
    if images is None:
        images = []
    
    message = {
        "role": "assistant",
        "content": content,
        "images": images
    }
    
    st.session_state[CHAT_HISTORY_KEY].append(message)


def get_chat_history() -> list:
    return st.session_state.get(CHAT_HISTORY_KEY, [])


def clear_chat_history() -> None:
    st.session_state[CHAT_HISTORY_KEY] = []