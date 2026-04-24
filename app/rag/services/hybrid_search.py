from langchain_core.documents import Document
from app.rag.db.mongo import mongodb_collection, mongodb_vector_store, keyword_search_index_name
from pathlib import Path
from sentence_transformers import CrossEncoder
import os

reranker_model = os.getenv("RERANKER_MODEL")

reranker = CrossEncoder(reranker_model)


def hybrid_search(
  query: str,
  user_id: str,
  file_name: str,
  top_k: int = 5
):
    ext = Path(file_name).suffix.lower()
    
    # Vector search
    vector_retrieved_docs = mongodb_vector_store.similarity_search(
        query = query,
        pre_filter = {
            "user_id": user_id,
            "source_type": ext[1:],
            "source_file": file_name
        },
        k = top_k
    )
    
    # keyword search
    keyword_pipeline = [
        {
            "$search": {
                "index": keyword_search_index_name,
                "compound": {
                    "should": [
                        {
                            "text": {
                                "query": query,
                                "path": "text"
                            }
                        }
                    ],
                    "filter": [
                        {"equals": {"path": "user_id", "value": user_id}},
                        {"equals": {"path": "source_type", "value": ext[1:]}},
                        {"equals": {"path": "source_file", "value": file_name}}
                    ]
                }
            }
        },
        {
            "$limit": top_k
        }
    ]

    docs = list(mongodb_collection.aggregate(keyword_pipeline))
    
    keyword_retrieved_docs = [
        Document(
            page_content = doc.get("page_content", ""),
            metadata = doc.get("metadata", {})
        )
        for doc in docs
    ]
    
    # combine both the retrieved docs
    retrieved_docs = vector_retrieved_docs + keyword_retrieved_docs
    # retrieved_docs = keyword_retrieved_docs
    
    return retrieved_docs

def rerank(query: str, docs: list[Document], top_k: int = 5):
    pairs = [(query, doc.page_content) for doc in docs]
    
    scores = reranker.predict(pairs)
    
    scored_docs = list(zip(docs, scores))
    
    reranked_docs = sorted(
        scored_docs,
        key = lambda x: x[1],
        reverse = True
    )
    
    return [doc for doc, _ in reranked_docs[:top_k]]