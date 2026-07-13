"""
Database connection stub.

This file will be updated once the database URL and ORM models
are shared by Intern 5.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Placeholder database URL
DATABASE_URL = "sqlite:///./app.db"

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Dependency for getting a database session.
    Replace DATABASE_URL with the production database
    once Intern 5 shares the connection details.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()