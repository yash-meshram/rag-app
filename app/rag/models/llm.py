import google.generativeai as google_genai
import os


# LLM client
_gemini_model = None
def _get_gemini():
    global _gemini_model
    if _gemini_model is None:
        google_genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
        _gemini_model = google_genai.GenerativeModel(
            model_name = os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-flash")
        )
    # logger.info("Gemini Vision model initialised")
    return _gemini_model

def get_gemini():
    return _get_gemini()