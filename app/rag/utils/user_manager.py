import uuid

def create_user_id() -> str:
    return str(uuid.uuid4())