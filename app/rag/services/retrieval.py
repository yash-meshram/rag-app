from db.mongo import mongodb_vector_store
from typing import List
from langchain_core.documents import Document

def retrieve_docs(query: str, user_id: str) -> List[Document]:
    retrieved_docs = mongodb_vector_store.similarity_search(
        query = query,
        filter = {"user_id": user_id},
        k = 5
    )
    return retrieved_docs