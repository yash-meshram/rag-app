from dotenv import load_dotenv
from rag.routes import query, upload
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

app.include_router(upload.router)
app.include_router(query.router)
