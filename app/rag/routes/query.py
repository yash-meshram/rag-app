from fastapi import APIRouter
from app.rag.services.retrieval import retrieve_docs
from app.rag.models.llm import get_model
from app.schemas.request import QuestionRequest

router = APIRouter()
llm = get_model()

@router.post("/query")
async def query(request: QuestionRequest):

    if request.file_name:
        docs, images = retrieve_docs(query = request.question, user_id = request.user_id, file_name = request.file_name)
        prompt = f"""
        Query: {request.question}
        Referance: {[doc.page_content for doc in docs]}
        """
        response = llm.invoke([prompt])
        return {"response": response.text, "images": images}
    else:
        response = llm.invoke([request.question])
        return {"response": response.text}