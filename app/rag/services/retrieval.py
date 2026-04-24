from typing import List
from langchain_core.documents import Document
from app.rag.models.llm import get_model
from app.rag.services.hybrid_search import hybrid_search, rerank

llm = get_model()

def get_enhanced_query(query: str) -> str:
    prompt = f"""You are a query enhancement assistant.
    Your job is to rewrite the user query to make it more detailed and specific for retrieving relevant documents.

    Rewrite the query by:
    1. Adding relevant technical terms
    2. Expanding abbreviations
    3. Including related concepts
    4. Being more specific and descriptive
    
    Original Query: {query}

    Return ONLY the enhanced query, nothing else. No explanation, no preamble.
    """
    response = llm.invoke([prompt])
    return response.text

def retrieve_docs(query: str, user_id: str, file_name: str, top_k: int = 5) -> List[Document]:
    enhanced_query = get_enhanced_query(query)
    
    retrieved_docs = hybrid_search(
        query = enhanced_query,
        user_id = user_id,
        file_name = file_name,
        top_k = top_k
    )
    
    reranked_retrieved_docs = rerank(query = query, docs = retrieved_docs, top_k = top_k)
    
    return reranked_retrieved_docs