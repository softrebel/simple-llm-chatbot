from typing import Literal
from app.graph.state import ChatState
import logging

logger = logging.getLogger(__name__)


def route_after_classification(state: ChatState) -> Literal["reject", "search"]:
    classification = state["classification"]
    logger.error("Classification started")
    if classification is None:
        logger.error("Classification result is missing")
        raise ValueError("Classification result is None")

    if classification.is_political:
        logger.info("Routing request to reject node")
        return "reject"

    logger.info("Routing request to search node")
    return "search"
