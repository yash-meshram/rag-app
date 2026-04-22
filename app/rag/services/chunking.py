from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

def chunk_text(document: List[Document], chunk_size: int = 500, chunk_overlap: int = 100) -> List[Document]:
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunks = splitter.split_documents(document)
    
    return chunks
