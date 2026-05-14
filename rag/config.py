from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    GROQ_API_KEY: str
    GEMINI_API_KEY: str
    HUGGINGFACE_API_KEY: str
    HF_TOKEN: str
    
    MONGODB_ATLAS_CLUSTER_URI: str
    MONGODB_ATLAS_DB: str
    MONGODB_ATLAS_COLLECTION: str
    VECTOR_SEARCH_INDEX_NAME: str
    KEYWORD_SEARCH_INDEX_NAME: str
    
    HUGGINGFACE_EMBEDDING_MODEL: str
    GEMINI_VISION_MODEL: str
    RERANKER_MODEL: str
    META_VISION_MODEL: str
    TEMPERATURE: float
    
    class Config:
        env_file = ".env"
        extra = "ignore"
        
settings = Settings()