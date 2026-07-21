"""
Day 10 — full learner journey smoke test.

Walks through the acceptance-criteria journey from the SRS (Section 9.2):
  register -> login -> browse lessons -> start a practice session ->
  submit an attempt -> get score/feedback -> check analytics

This is a SMOKE test, not a full test suite — it just proves the live,
deployed pieces actually talk to each other end-to-end. Real functional
testing of each API is each intern's own responsibility (Intern 2 for
Auth/Course, Intern 4 for Assessment/Feedback/Analytics, etc.).

Endpoint paths below are best guesses based on the SRS's functional
requirements — confirm the exact paths with Intern 2 / Intern 4's Swagger
docs (from Day 10 of their tracks) and adjust the constants at the top
before running against the real deployment.

Run:
    python scripts/smoke_test_full_journey.py --base-url https://sign-language-backend.onrender.com
"""

import argparse
import sys
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json

# --- Adjust these to match the real, frozen API from Day 10 ---
REGISTER_PATH = "/api/auth/register"
LOGIN_PATH = "/api/auth/login"
LESSONS_PATH = "/api/lessons"
PRACTICE_START_PATH = "/api/practice/start"
PRACTICE_SUBMIT_PATH = "/api/practice/submit"
ANALYTICS_PATH = "/api/analytics/summary"


def call(method: str, url: str, token: str = None, body: dict = None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=15) as response:
            raw = response.read()
            return response.status, (json.loads(raw) if raw else {})
    except HTTPError as exc:
        raw = exc.read()
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, {"raw": raw.decode(errors="replace")}
    except URLError as exc:
        return None, {"error": str(exc)}


def step(label: str, ok: bool, detail: str = ""):
    status = "OK" if ok else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke test the full learner journey.")
    parser.add_argument("--base-url", required=True, help="Live backend base URL")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    results = []
    test_email = f"smoketest_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "SmokeTest123!"

    # 1. Register
    status, body = call(
        "POST", base + REGISTER_PATH,
        body={"name": "Smoke Test", "email": test_email, "password": test_password, "role": "learner"},
    )
    results.append(step("Register", status in (200, 201), f"status={status}"))

    # 2. Login
    status, body = call("POST", base + LOGIN_PATH, body={"email": test_email, "password": test_password})
    token = body.get("access_token") or body.get("token")
    results.append(step("Login", status == 200 and bool(token), f"status={status}"))

    if not token:
        print("\nCan't continue without a token — stopping here.")
        print(f"{results.count(False)} check(s) failed out of {len(results)}.")
        sys.exit(1)

    # 3. Browse lessons
    status, body = call("GET", base + LESSONS_PATH, token=token)
    lessons = body if isinstance(body, list) else body.get("items", [])
    results.append(step("Browse lessons", status == 200 and len(lessons) > 0, f"status={status}, count={len(lessons)}"))

    lesson_id = lessons[0]["id"] if lessons else None

    # 4. Start a practice session
    status, body = call("POST", base + PRACTICE_START_PATH, token=token, body={"lesson_id": lesson_id})
    session_id = body.get("session_id") or body.get("id")
    results.append(step("Start practice session", status in (200, 201) and bool(session_id), f"status={status}"))

    # 5. Submit an attempt (mock prediction — real one comes from the AI service)
    status, body = call(
        "POST", base + PRACTICE_SUBMIT_PATH, token=token,
        body={"session_id": session_id, "predicted_sign": "A", "confidence": 0.9},
    )
    has_score = "accuracy_score" in body or "score" in body
    results.append(step("Submit attempt -> get score/feedback", status == 200 and has_score, f"status={status}"))

    # 6. Analytics reflects the attempt
    status, body = call("GET", base + ANALYTICS_PATH, token=token)
    results.append(step("Analytics summary reachable", status == 200, f"status={status}"))

    print()
    passed = results.count(True)
    print(f"{passed}/{len(results)} checks passed.")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
