from pymongo import MongoClient
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from app.rag.services.embedding import embedding
import certifi

cluster_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
db_name = os.getenv("MONGODB_ATLAS_DB")
collection_name = os.getenv("MONGODB_ATLAS_COLLECTION")
vector_search_index_name = os.getenv("VECTOR_SEARCH_INDEX_NAME")
keyword_search_index_name = os.getenv("KEYWORD_SEARCH_INDEX_NAME")

client = MongoClient(
    cluster_uri,
    tls=True,
    tlsCAFile = certifi.where()
)
mongodb_db = client[db_name]
mongodb_collection = mongodb_db[collection_name]

# vector store
mongodb_vector_store = MongoDBAtlasVectorSearch(
    embedding = embedding,
    collection = mongodb_collection,
    index_name = vector_search_index_name,
    relevance_score_fn = "cosine"
)