from fastapi import APIRouter, HTTPException

from app.api.models import ChatRequest, ChatResponse
from app.graph.graph import build_graph
import logging

router = APIRouter(prefix="/api/v1", tags=["chat"])

graph = build_graph()


logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    logger.info(f"Received chat request | question= {request.question}")
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

        logger.info(
            f"Chat request completed successfully | question= {request.question}  | answer= {result['answer']}"
        )

        return ChatResponse(
            answer=result["answer"], classification_result=result["classification"]
        )

    except Exception as exc:
        logger.exception(f"Chat request failed | error= {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail="خطایی در پردازش درخواست رخ داد.",
        ) from exc
