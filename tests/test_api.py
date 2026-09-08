from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_empty_question():
    response = client.post("/api/v1/chat", json={"question": ""})

    assert response.status_code == 422


def test_chat_too_long_question():
    response = client.post("/api/v1/chat", json={"question": "a" * 100000})

    assert response.status_code == 422


def test_chat_api():
    fake_result = {
        "answer": "جمعیت ایران بیش از 92 میلیون نفر است.",
        "classification": {
            "is_political": False,
            "confidence": 0.9,
            "entities": [
                {
                    "text": "ایران",
                    "type": "COUNTRY",
                }
            ],
            "concepts": [
                "جمعیت ایران",
                "آمار جمعیت",
                "ایران",
                "نقشه ایران",
                "اقتصاد ایران",
            ],
            "reason": (
                "The question is asking about the population of Iran, "
                "which is a demographic inquiry and does not involve "
                "political aspects."
            ),
        },
        "search_results": [],
        "error": None,
    }

    with patch(
        "app.api.routes.graph.invoke",
        return_value=fake_result,
    ):
        response = client.post(
            "/api/v1/chat",
            json={"question": "جمعیت ایران چقدر است؟"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "جمعیت ایران بیش از 92 میلیون نفر است.",
        "classification_result": {
            "is_political": False,
            "confidence": 0.9,
            "entities": [
                {
                    "text": "ایران",
                    "type": "COUNTRY",
                }
            ],
            "concepts": [
                "جمعیت ایران",
                "آمار جمعیت",
                "ایران",
                "نقشه ایران",
                "اقتصاد ایران",
            ],
            "reason": (
                "The question is asking about the population of Iran, "
                "which is a demographic inquiry and does not involve "
                "political aspects."
            ),
        },
    }


def test_political_chat_api():
    fake_result = {
        "answer": "متاسفانه اجازه پاسخ دادن به این سوال را ندارم.",
        "classification": {
            "is_political": True,
            "confidence": 0.99,
            "entities": [
                {
                    "text": "آمریکا",
                    "type": "COUNTRY",
                }
            ],
            "concepts": [],
            "reason": "The question concerns a political topic.",
        },
        "search_results": [],
        "error": None,
    }

    with patch(
        "app.api.routes.graph.invoke",
        return_value=fake_result,
    ):
        response = client.post(
            "/api/v1/chat",
            json={"question": "رئیس جمهور آمریکا کیست؟"},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == ("متاسفانه اجازه پاسخ دادن به این سوال را ندارم.")

    assert data["classification_result"]["is_political"] is True
