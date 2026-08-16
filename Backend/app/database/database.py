import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Repository root
BASE_DIR = Path(__file__).resolve().parents[3]

# Add Database_Devops to Python path
DB_PROJECT = BASE_DIR / "Database_Devops"
sys.path.append(str(DB_PROJECT))

# Load .env from repo root
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError(
        f"DATABASE_URL not found. Expected .env at: {BASE_DIR / '.env'}"
    )

# SQLite needs check_same_thread=False for FastAPI's threading model.
# PostgreSQL doesn't use connect_args so the dict is harmless either way.
_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)

# Verify connection with a DB-agnostic query
from sqlalchemy import text
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Database connection OK")
except Exception as exc:
    print(f"Database connection failed: {exc}")

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
