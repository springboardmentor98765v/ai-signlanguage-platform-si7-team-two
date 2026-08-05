import uuid
from fastapi.testclient import TestClient


def test_register_login_journey(client: TestClient):
    """
    Full user journey:
    Register -> Login -> Receive JWT token
    """

    email = f"journey_{uuid.uuid4().hex[:8]}@example.com"
    password = "Password123"

    # Step 1: Register
    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Journey User",
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    registered_user = register_response.json()

    assert registered_user["email"] == email


    # Step 2: Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert login_data["message"] == "Login successful"
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"