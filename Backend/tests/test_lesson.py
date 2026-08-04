from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_lesson():
    response = client.post(
        "/lessons/",
        json={
            "course_id": "invalid-uuid",
            "letter": "",
            "title": "A",
            "description": "Test",
            "reference_image_url": "",
            "order_index": 0,
        },
    )

    assert response.status_code == 422


def test_invalid_lesson_id():
    response = client.get("/lessons/invalid-uuid")

    assert response.status_code == 422