from typing import List
from langchain_core.documents import Document
from db.mongo import mongodb_vector_store


def store_document(user_id: str, chunks: List[Document]):
    # adding document into vector store
    mongodb_vector_store.add_documents(chunks)