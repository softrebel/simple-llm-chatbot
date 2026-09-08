import json
from pathlib import Path

from app.llm.client import create_classifier

from app.llm.prompts import POLITICAL_CLASSIFIER_SYSTEM_PROMPT
from langchain_core.messages import HumanMessage, SystemMessage
from app.models.classification import ClassificationResult


def load_test_cases():
    path = Path(__file__).parent / "test_cases.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_classifier():
    classifier = create_classifier()
    cases = load_test_cases()
    failures = []
    for case in cases:
        result: ClassificationResult = classifier.invoke(
            [
                SystemMessage(content=POLITICAL_CLASSIFIER_SYSTEM_PROMPT),
                HumanMessage(content=case["question"]),
            ]
        )

        expected = case["expected_political"]

        if result.is_political != expected:
            failures.append(
                {
                    "question": case["question"],
                    "expected": expected,
                    "actual": result.is_political,
                }
            )

    assert not failures, failures
