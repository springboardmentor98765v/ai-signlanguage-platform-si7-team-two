from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_invalid_register_email():
    response = client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "abc",
            "password": "Password123",
        },
    )

    assert response.status_code == 422


def test_invalid_register_password():
    response = client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "12345",
        },
    )

    assert response.status_code == 422


def test_invalid_register_name():
    response = client.post(
        "/auth/register",
        json={
            "full_name": "   ",
            "email": "john@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 422
