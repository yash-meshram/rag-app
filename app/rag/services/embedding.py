from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from langchain_huggingface import HuggingFaceEmbeddings

embeding_model = os.getenv("EMBEDDING_MODEL")
huggingface_embeding_model = os.getenv("HUGGINGFACE_EMBEDDING_MODEL")

embedding = HuggingFaceEmbeddings(model_name = huggingface_embeding_model)
model = SentenceTransformer(embeding_model)

def get_embedding(texts: List[str]) -> np.ndarray:
    embeddings = model.encode(texts, batch_size = 32, normalize_embeddings = True)
    return embeddings