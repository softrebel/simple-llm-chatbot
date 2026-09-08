from langchain_core.messages import HumanMessage, SystemMessage

from app.graph.state import ChatState
from app.llm.client import create_classifier, create_llm
from app.llm.prompts import ANSWER_SYSTEM_PROMPT, POLITICAL_CLASSIFIER_SYSTEM_PROMPT
from app.search.base import SearchEngine


REJECTION_MESSAGE = "متاسفانه اجازه پاسخ دادن به این سوال را ندارم."


class ClassifierNode:
    def __init__(self):
        self.classifier = create_classifier()

    def __call__(self, state: ChatState):
        question = state["question"]
        result = self.classifier.invoke(
            [
                SystemMessage(content=POLITICAL_CLASSIFIER_SYSTEM_PROMPT),
                HumanMessage(content=question),
            ]
        )

        return {"classification": result}


class RejectNode:
    def __call__(self, state: ChatState):
        return {"answer": REJECTION_MESSAGE}


class SearchNode:
    def __init__(self, search_engine: SearchEngine):
        self.search_engine = search_engine

    def __call__(self, state: ChatState):
        question = state["question"]

        results = self.search_engine.search(question)

        return {"search_results": results}


class AnswerNode:
    def __init__(self):
        self.llm = create_llm()

    def __call__(self, state: ChatState):
        question = state["question"]
        results = state["search_results"]

        if not results:
            return {"answer": "اطلاعات کافی برای پاسخ به این سوال یافت نشد."}

        context = self._build_context(results)
        response = self.llm.invoke(
            [
                SystemMessage(content=ANSWER_SYSTEM_PROMPT),
                HumanMessage(
                    content=(f"Question:\n{question}\n\nSearch results:\n{context}")
                ),
            ]
        )
        return {"answer": response.content}

    @staticmethod
    def _build_context(results: list[dict]) -> str:
        chunks = []

        for index, result in enumerate(results, start=1):
            chunks.append(
                f"""
                    Result {index}
                    Title: {result.get("title", "")}
                    Content: {result.get("snippet", "")}
                """.strip()
            )

        return "\n\n".join(chunks)
