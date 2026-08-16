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

# Load .env
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError(
        f"DATABASE_URL not found. Expected .env at: {BASE_DIR / '.env'}"
    )

print("DATABASE_URL =", DATABASE_URL)

engine = create_engine(DATABASE_URL)
from sqlalchemy import text

with engine.connect() as conn:
    print("Connected Database:", conn.execute(text("SELECT current_database()")).scalar())
    print("Current Schema:", conn.execute(text("SELECT current_schema()")).scalar())

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