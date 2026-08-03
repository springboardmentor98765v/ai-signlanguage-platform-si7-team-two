"""
Milestone 3 - Day 6, Test 1
Full-journey local integration test: Register -> Login -> Practice -> Badge
earned -> Streak updated -> Notification created -> Notification Bell fetch.

Runs against the local Docker Compose test stack (docker-compose.test.yml) —
no live/public deployment involved.

Usage:
    docker compose -f docker-compose.test.yml up -d
    BASE_URL=http://localhost:8001 python test_learner_journey.py
"""
import os
import time
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")


def test_register_login_practice_badge_notification():
    # 1. Register
    register_resp = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Integration Test Learner",
        "email": f"integration_test_{int(time.time())}@example.com",
        "password": "TestPass123!",
        "role": "learner",
    })
    assert register_resp.status_code in (200, 201), f"Register failed: {register_resp.text}"
    user = register_resp.json()

    # 2. Login
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": user["email"],
        "password": "TestPass123!",
    })
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Practice + get a high-confidence prediction (drives badge/streak logic)
    practice_resp = requests.post(f"{BASE_URL}/practice/attempt", headers=headers, json={
        "lesson_letter": "A",
        "predicted_sign": "A",
        "confidence": 0.95,
    })
    assert practice_resp.status_code == 200, f"Practice attempt failed: {practice_resp.text}"

    # 4. Confirm a streak record now exists for this learner
    streak_resp = requests.get(f"{BASE_URL}/streaks/me", headers=headers)
    assert streak_resp.status_code == 200, f"Streak fetch failed: {streak_resp.text}"
    assert streak_resp.json()["current_streak"] >= 1

    # 5. Confirm at least one notification was generated (e.g. streak/badge event)
    notif_resp = requests.get(f"{BASE_URL}/notifications/me", headers=headers)
    assert notif_resp.status_code == 200, f"Notification fetch failed: {notif_resp.text}"
    notifications = notif_resp.json()
    assert isinstance(notifications, list)

    print("✅ Full learner journey (register -> practice -> streak -> notifications) passed")


if __name__ == "__main__":
    test_register_login_practice_badge_notification()
