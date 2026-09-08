from typing import TypedDict
from app.models.classification import ClassificationResult


class ChatState(TypedDict):
    question: str
    classification: ClassificationResult | None
    search_results: list[dict]
    answer: str
    error: str | None
