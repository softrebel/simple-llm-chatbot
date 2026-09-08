from pydantic import BaseModel, Field
from app.models.classification import ClassificationResult


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    classification_result: ClassificationResult
