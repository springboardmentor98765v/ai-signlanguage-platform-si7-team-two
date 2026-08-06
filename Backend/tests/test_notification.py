from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_notification_invalid_uuid():
    response = client.get("/notifications/notifications/invalid-uuid")

    assert response.status_code == 422


def test_notification_invalid_body():
    response = client.post(
        "/notifications/notifications/",
        json={
            "user_id": "invalid-uuid",
            "title": "",
            "message": "Hi"
        },
    )

    assert response.status_code == 422