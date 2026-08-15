from fastapi.testclient import TestClient

# Existing lesson ID from your database
LESSON_ID = "096fca1b-1e20-4417-b3e0-5b19d4f94d55"


def test_get_all_lessons(client: TestClient):
    response = client.get("/lessons/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]

    assert "id" in first
    assert "title" in first
    assert "letter" in first
    assert "course_id" in first
    assert "order_index" in first


def test_get_single_lesson(client: TestClient):
    response = client.get(f"/lessons/{LESSON_ID}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == LESSON_ID
    assert data["letter"] == "A"
    assert data["title"] == "Letter A"


def test_get_invalid_lesson(client: TestClient):
    response = client.get("/lessons/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"
