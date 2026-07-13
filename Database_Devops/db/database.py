"""
db/database.py

SQLAlchemy engine + session factory, reading connection details from the
same .env used by Day 2's Docker Compose setup (DATABASE_URL). This is the
one place engine configuration lives — Intern 2's FastAPI app should import
`get_session` from here rather than creating its own engine, so there's a
single source of truth for how the app connects to Postgres.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Load the repo-root .env regardless of what directory this is run from.

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL =", DATABASE_URL)

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL not found in .env")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env at the repo "
        "root (or use the shared Day 2 .env) before running anything here."
    )

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session() -> Session:
    """Returns a new SQLAlchemy session. Caller is responsible for closing it
    (or use it as a context manager: `with get_session() as session:`)."""
    return SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
