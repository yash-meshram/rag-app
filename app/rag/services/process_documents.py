from langchain_core.documents import Document
from logger_config import get_logger
from typing import List
import fitz
from services.image_handler import bytes_to_pil, pil_to_base64, get_image_description


# logger
logger = get_logger(__name__)


# Loading and parsing PDF file
def load_pdf(file_path: str, user_id: str) -> List[Document]:
    """Load the pdf file and parse into pdf_data"""
    pdf_data: List[Document] = []
    doc = fitz.open(file_path)
    source_file = file_path.split("/")[-1]
    
    for page_num, page in enumerate(doc, start = 1):
        # Handling Text
        text = page.get_text("text").strip()
        if text:
            pdf_data.append(Document(
                page_content = text,
                metadata = {
                    "user_id": user_id,
                    "source_type": "pdf",
                    "source_file": source_file,
                    "page_number": page_num,
                    "content_type": "text"
                }
            ))
        
        # Handling Image
        image_list = page.get_images(full = True)
        for image_index, image_info in enumerate(image_list, start = 1):
            xref = image_info[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # convert bytes images to pil
                pil_image = bytes_to_pil(image_bytes)
                
                # skip the tiny images, logs, etc
                if pil_image.width < 50 or pil_image.height < 50:
                    continue
                
                # convert pil image to base64
                image_b64 = pil_to_base64(pil_image)
                
                # get image description
                image_description = get_image_description(
                    image_b64 = image_b64,
                    context = f"Image {image_index} from page {page_num} of {source_file}"
                )
                
                pdf_data.append(Document(
                    page_content = image_description,
                    metadata = {
                        "user_id": user_id,
                        "source_type": "pdf",
                        "source_file": source_file,
                        "page_number": page_num,
                        "content_type": "image",
                        "image_data": image_b64,
                        "image_index": image_index,
                        "image_ext": image_ext,
                        "image_width": pil_image.width,
                        "image_height": pil_image.height
                    }
                ))
            except Exception as e:
                logger.warning(f"Failed to extract image xref = {xref} from page {page_num} of {source_file}: {e}")
    
    doc.close()
    logger.info(f"{source_file} loaded and parsed to {len(pdf_data)} raw blocks")
    return pdf_data


# Loading and parsing DOC file


# Loading and parsing standalone Image file


# Loading and parsing excel file