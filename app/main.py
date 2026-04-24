from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.rag.routes import upload, query


app = FastAPI()

app.include_router(upload.router)
app.include_router(query.router)