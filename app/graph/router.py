from typing import Literal
from app.graph.state import ChatState


def route_after_classification(state: ChatState) -> Literal["reject", "search"]:
    classification = state["classification"]
    if classification is None:
        raise ValueError("Classification result is None")

    if classification.is_political:
        return "reject"

    return "search"


