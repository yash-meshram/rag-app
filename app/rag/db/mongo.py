from pymongo import MongoClient
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from services.embedding import embedding

cluster_uri = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
db_name = os.getenv("MONGODB_ATLAS_DB")
collection_name = os.getenv("MONGODB_ATLAS_COLLECTION")
index_name = os.getenv("MONGODB_ATLAS_INDEX")

client = MongoClient(cluster_uri)
mongodb_collection = client[db_name][collection_name]
vector_search_index_name = "rag_app_id"

# vector store
mongodb_vector_store = MongoDBAtlasVectorSearch(
    embedding = embedding,
    collection = mongodb_collection,
    index_name = vector_search_index_name,
    relevance_score_fn = "cosine"
)