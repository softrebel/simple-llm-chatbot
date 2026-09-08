from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.classification import ClassificationResult


def create_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.model_name,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        temperature=0,
    )


def create_classifier():
    llm = create_llm()

    return llm.with_structured_output(ClassificationResult)
