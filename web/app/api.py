from typing import Dict, Any
import requests
from app.config import api_base_url

def api_query(query: str, user_id: str = "", file_name: str = "") -> Dict[str, Any]:
    endpoint = f"{api_base_url}/query"
    payload = {
        "question": query,
        "user_id": user_id,
        "file_name": file_name
    }
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    return response.json()


def api_upload(file) -> str:
    endpoint = f"{api_base_url}/upload"
    files = {
        "file": (file.name, file, file.type)
    }
    response = requests.post(endpoint, files=files)
    response.raise_for_status()
    return response.json()['user_id']