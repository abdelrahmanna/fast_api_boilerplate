"""
Tests for the User API endpoints.
"""

from fastapi.testclient import TestClient
from main import app
from app.core.config import settings

client = TestClient(app)


def test_create_and_get_user():
    response = client.post(
        settings.BASE_API + "/users/",
        json={
            "email": "test@example.com",
            "hashed_password": "password123",
            "is_active": True,
            "username": "testuser",
            "full_name": "Test User",
            "is_verified": True,
        },
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test@example.com"
    user_id = user["id"]

    response = client.get(f"{settings.BASE_API}/users/{user_id}")
    assert response.status_code == 200
    fetched_user = response.json()
    assert fetched_user["email"] == "test@example.com"
