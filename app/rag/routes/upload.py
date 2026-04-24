from fastapi import APIRouter, UploadFile
from app.rag.utils.user_manager import create_user_id
from app.rag.services.ingestion import store_document

import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):

    user_id = create_user_id()

    file_path = f"app/data/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    store_document(file_path = file_path, user_id = user_id)

    os.remove(file_path)

    return {"user_id": user_id, "file_name": file.filename}