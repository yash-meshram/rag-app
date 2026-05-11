from dotenv import load_dotenv
load_dotenv()

from app import query
from app import upload
from fastapi import FastAPI

app = FastAPI()

app.include_router(upload.router)
app.include_router(query.router)
