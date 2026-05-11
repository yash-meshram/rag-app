# from sentence_transformers import SentenceTransformer
import os
from langchain_huggingface import HuggingFaceEmbeddings

# huggingface_embeding_model = "sentence-transformers/all-MiniLM-L6-v2"
huggingface_embeding_model = os.getenv("HUGGINGFACE_EMBEDDING_MODEL")

embedding = HuggingFaceEmbeddings(model_name = huggingface_embeding_model)
# model = SentenceTransformer(embeding_model)