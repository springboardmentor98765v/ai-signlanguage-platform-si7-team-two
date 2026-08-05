from fastapi.testclient import TestClient


def test_user_lesson_journey(client: TestClient):
    """
    Full lesson journey:
    View lessons -> Open lesson
    """

    # Step 1: View all lessons
    lessons_response = client.get("/lessons/")

    assert lessons_response.status_code == 200

    lessons = lessons_response.json()

    assert len(lessons) > 0


    # Step 2: Pick first lesson
    lesson_id = lessons[0]["id"]


    # Step 3: Open lesson
    lesson_response = client.get(
        f"/lessons/{lesson_id}"
    )

    assert lesson_response.status_code == 200

    lesson = lesson_response.json()

    assert lesson["id"] == lesson_id
    assert "title" in lesson
    assert "letter" in lesson