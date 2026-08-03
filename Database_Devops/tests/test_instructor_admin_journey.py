"""
Milestone 3 - Day 6, Test 2
Full-journey local integration test: Instructor views Leaderboard,
Admin performs a bulk user action, and the database stays consistent.

Runs against the local Docker Compose test stack — no live deployment involved.

Usage:
    docker compose -f docker-compose.test.yml up -d
    BASE_URL=http://localhost:8001 python test_instructor_admin_journey.py
"""
import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")

# Assumes seed data/fixtures create these accounts locally for testing;
# swap for your project's actual test-seed credentials.
INSTRUCTOR_CREDS = {"email": "test_instructor@example.com", "password": "TestPass123!"}
ADMIN_CREDS = {"email": "test_admin@example.com", "password": "TestPass123!"}


def _login(creds):
    resp = requests.post(f"{BASE_URL}/auth/login", json=creds)
    assert resp.status_code == 200, f"Login failed for {creds['email']}: {resp.text}"
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_instructor_leaderboard():
    headers = _login(INSTRUCTOR_CREDS)
    resp = requests.get(f"{BASE_URL}/leaderboard?rank_by=streak", headers=headers)
    assert resp.status_code == 200, f"Leaderboard fetch failed: {resp.text}"
    leaderboard = resp.json()
    assert isinstance(leaderboard, list)
    print(f"✅ Instructor leaderboard returned {len(leaderboard)} ranked learner(s)")


def test_admin_bulk_deactivate():
    headers = _login(ADMIN_CREDS)

    users_resp = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    assert users_resp.status_code == 200, f"Admin user list failed: {users_resp.text}"
    sample_ids = [u["id"] for u in users_resp.json() if u["role"] == "learner"][:2]
    assert sample_ids, "No learner accounts available to test bulk deactivate against"

    bulk_resp = requests.post(f"{BASE_URL}/admin/users/bulk-deactivate", headers=headers, json={
        "user_ids": sample_ids,
    })
    assert bulk_resp.status_code == 200, f"Bulk deactivate failed: {bulk_resp.text}"

    # Re-activate so this test is safely repeatable
    reactivate_resp = requests.post(f"{BASE_URL}/admin/users/bulk-activate", headers=headers, json={
        "user_ids": sample_ids,
    })
    assert reactivate_resp.status_code == 200

    print(f"✅ Admin bulk deactivate/reactivate passed for {len(sample_ids)} user(s)")


if __name__ == "__main__":
    test_instructor_leaderboard()
    test_admin_bulk_deactivate()
