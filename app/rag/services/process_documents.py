from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
import os

def load_pdf(file_path) -> List[Document]:
    # loading the pdf file
    loader = PyMuPDFLoader(file_path)
    document = loader.load()
    
    # adding metadata custom
    for page in document:
        page.metadata["file_type"] = "pdf"
        page.metadata["file_name"] = os.path.basename(file_path)
        page.metadata["content_type"] = "text"
                    
    return document