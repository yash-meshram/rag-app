from app.rag.services.process_documents import load_document
from app.rag.services.chunking import chunk_document
from app.rag.db.mongo import mongodb_vector_store


def store_document(file_path: str, user_id: str):
    # loading the document
    document = load_document(file_path = file_path, user_id = user_id)
    
    # splitting the documenst into chunks
    chunks = chunk_document(document = document)
    
    # adding chunks into vector store
    mongodb_vector_store.add_documents(chunks)