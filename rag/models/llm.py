# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os


# LLM client
_model = None
def _get_model():
    global _model
    if _model is None:
        # _gemini_model = ChatGoogleGenerativeAI(model = os.getenv("GEMINI_VISION_MODEL"))
        _model = ChatGroq(model = os.getenv("META_VISION_MODEL"), temperature = 0.2)
    return _model

def get_model():
    return _get_model()