import uuid

from fastapi.testclient import TestClient


def create_test_user(client: TestClient):
    """
    Registers a fresh user and returns email/password.
    """
    email = f"pytest_{uuid.uuid4().hex[:8]}@example.com"
    password = "Password123"

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Pytest User",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    return email, password


def test_root(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Backend API is running successfully!"


def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "backend"
    assert data["version"] == "1.0.0"


def test_register_user(client: TestClient):
    email = f"pytest_{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "full_name": "Pytest User",
            "email": email,
            "password": "Password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Pytest User"
    assert data["email"] == email
    assert "id" in data
    assert "role_id" in data


def test_login_user(client: TestClient):
    email, password = create_test_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == email


def test_invalid_login(client: TestClient):
    email, password = create_test_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"



def test_update_profile(client: TestClient):
    

    # Register a new user
    email = f"profile_{uuid.uuid4().hex[:8]}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Original Name",
            "email": email,
            "password": "Password123",
        },
    )

    assert register_response.status_code == 201

    user = register_response.json()
    user_id = user["id"]

    # Update profile
    response = client.put(
        f"/auth/profile/{user_id}",
        json={
            "full_name": "Updated Name",
            "email": email,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["full_name"] == "Updated Name"
    assert data["email"] == email



def test_change_password(client: TestClient):
    email = f"changepass_{uuid.uuid4().hex[:8]}@example.com"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Password User",
            "email": email,
            "password": "OldPassword123",
        },
    )

    assert register_response.status_code == 201

    user = register_response.json()
    user_id = user["id"]

    # Change password
    response = client.put(
        f"/auth/change-password/{user_id}",
        json={
            "old_password": "OldPassword123",
            "new_password": "NewPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Password changed successfully"

    # Verify login with new password
    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "NewPassword123",
        },
    )

    assert login_response.status_code == 200