from PIL import Image
import io
import base64
from models.llm import get_gemini
from logger_config import get_logger

# logger
logger = get_logger(__name__)


# Image handling helper
def _bytes_to_pil(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")


def _pil_to_base64(pil_image: Image.Image, format: str = "png") -> str:
    # Creates a temporary memory space (like a file, but in RAM). No file is written to disk
    buf = io.BytesIO()
    pil_image.save(buf, format = format)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _base64_to_pil(image_b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGB")


def _get_image_description(image_b64: str, context: str = "") -> str:
    prompt = """Describe this image in detail for a semantic search index.
    Include: all visible text (OCR), objects, charts, diagrams, tables, key data points, colors, layout, and any domain-specific content.
    Be thorough — your description will be the sole representation of this image in a retrieval system.
    """
    
    if context:
        prompt = f"Context: {context}\n\n{prompt}"
       
    try:
        llm = get_gemini()
        # Gemini accept PIL image directly - no base64 encoding needed
        pil_image = _base64_to_pil(image_b64)
        response = llm.generate_content([prompt, pil_image])
        return response.text
    except Exception as e:
        logger.error(f"Gemini vision description failed: {e}")
        return "Image content (description unavailable)"


def bytes_to_pil(image_bytes: bytes) -> Image.Image:
    return _bytes_to_pil(image_bytes = image_bytes)

def pil_to_base64(pil_image: Image.Image, format: str = "png") -> str:
    return _pil_to_base64(pil_image = pil_image, format = format)

def base64_to_pil(image_b64: str) -> Image.Image:
    return _base64_to_pil(image_b64 = image_b64)

def get_image_description(image_b64: str, context: str = "") -> str:
    return _get_image_description(image_b64 = image_b64, context = context)