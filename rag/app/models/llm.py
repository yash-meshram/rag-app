from config import settings
from langchain_groq import ChatGroq


# LLM client
_model = None
def _get_model():
    global _model
    if _model is None:
        # _gemini_model = ChatGoogleGenerativeAI(model = os.getenv("GEMINI_VISION_MODEL"))
        _model = ChatGroq(
            api_key = settings.GROQ_API_KEY,
            model = settings.META_VISION_MODEL,
            temperature = settings.TEMPERATURE
        )
    return _model

def get_model():
    return _get_model()