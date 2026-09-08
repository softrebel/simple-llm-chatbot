from app.graph.router import route_after_classification
from app.models.classification import (
    ClassificationResult,
)


def test_political_route():

    state = {
        "question": "رئیس جمهور آمریکا کیست؟",
        "classification": ClassificationResult(
            is_political=True,
            confidence=0.99,
            entities=[],
            reason="Political person",
        ),
        "search_results": [],
        "answer": "",
        "error": None,
    }

    assert route_after_classification(
        state
    ) == "reject"


def test_non_political_route():

    state = {
        "question": "پایتخت فرانسه کجاست؟",
        "classification": ClassificationResult(
            is_political=False,
            confidence=0.99,
            entities=[],
            reason="Geographical question",
        ),
        "search_results": [],
        "answer": "",
        "error": None,
    }

    assert route_after_classification(
        state
    ) == "search"
