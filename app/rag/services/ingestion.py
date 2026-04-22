from typing import List
from langchain_core.documents import Document
from db.mongo import mongodb_vector_store


def prepare_document(user_id: str, chunks: List[Document]) -> List[Document]:
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "user_id": user_id,
            "file_type": chunk.metadata['file_type'],
            "file_name": chunk.metadata['file_name'],
            "content_type": chunk.metadata['content_type'],
            "chunk_id": i
        })
    return chunks


def store_document(user_id: str, chunks: List[Document]):
    # prepare document
    document = prepare_document(user_id, chunks)
    
    # adding document into vector store
    mongodb_vector_store.add_documents(document)
    
    
    