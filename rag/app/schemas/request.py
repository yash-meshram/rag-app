from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    file_name: str
    user_id: str
    
class UploadFileRequest(BaseModel):
    file_name: str
