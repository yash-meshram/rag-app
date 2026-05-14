from config import settings
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from app.services.embedding import embedding
import certifi

cluster_uri = settings.MONGODB_ATLAS_CLUSTER_URI
db_name = settings.MONGODB_ATLAS_DB
collection_name = settings.MONGODB_ATLAS_COLLECTION
vector_search_index_name = settings.VECTOR_SEARCH_INDEX_NAME
keyword_search_index_name = settings.KEYWORD_SEARCH_INDEX_NAME

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