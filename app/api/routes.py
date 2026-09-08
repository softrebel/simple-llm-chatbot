from fastapi import APIRouter, HTTPException

from app.api.models import ChatRequest, ChatResponse
from app.graph.graph import build_graph


router = APIRouter(prefix="/api/v1", tags=["chat"])

graph = build_graph()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = graph.invoke(
            {
                "question": request.question,
                "classification": None,
                "search_results": [],
                "answer": "",
                "error": None,
            }
        )

        return ChatResponse(
            answer=result["answer"], classification_result=result["classification"]
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="خطایی در پردازش درخواست رخ داد.",
        ) from exc
