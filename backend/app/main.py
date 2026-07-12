"""
backend/app/main.py

PLACEHOLDER backend service. Intern 2 owns the real User/Course APIs
(SRS §6, Intern 2) — this stub exists only so Day 5's Docker Compose stack
has something real to build, run, and health-check against, proving the
containerization actually works end to end before real endpoints exist.

Replace/extend this file with the real FastAPI app; keep `/health` and
`/health/db` as-is if convenient (Day 7's integration check depends on
them), or move their logic into whatever router structure Intern 2 sets up.
"""
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from db.database import engine

app = FastAPI(title="Sign Language Platform — Backend (PLACEHOLDER)")


@app.get("/health")
def health():
    return {"status": "ok", "service": "backend", "note": "placeholder service — Intern 2's real API replaces this"}


@app.get("/health/db")
def health_db():
    """Proves the backend container can actually reach the Postgres
    container over the Docker network and query real seeded data —
    this is the concrete "verify DB connections end-to-end" check
    referenced in SRS Day 7."""
    try:
        with engine.connect() as conn:
            roles_count = conn.execute(text("SELECT COUNT(*) FROM roles")).scalar_one()
            lessons_count = conn.execute(text("SELECT COUNT(*) FROM lessons")).scalar_one()
        return {
            "status": "ok",
            "roles_count": roles_count,
            "lessons_count": lessons_count,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {exc}")
