from fastapi import FastAPI, HTTPException
from sqlalchemy import text

# Harshit's DB health check
from app.database.database import engine

# Your routers
from app.routers import auth
from app.routers import practice

# Your middleware
from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit

app = FastAPI(
    title="AI-Powered Sign Language Learning & Assessment Platform",
    description="Backend API for Sign Language Learning & Assessment Platform.",
    version="1.0.0",
)

# Middleware
app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(practice.router, prefix="/practice", tags=["Practice"])


@app.get("/")
def root():
    return {"message": "Backend API is running successfully!"}


@app.get("/health")
def health():
    return {"status": "healthy", "service": "backend", "version": "1.0.0"}


@app.get("/health/db")
def health_db():
    """
    Checks database connectivity and seeded tables.
    """
    try:
        with engine.connect() as conn:
            roles_count = conn.execute(text("SELECT COUNT(*) FROM roles")).scalar_one()

            lessons_count = conn.execute(
                text("SELECT COUNT(*) FROM lessons")
            ).scalar_one()

        return {
            "status": "ok",
            "roles_count": roles_count,
            "lessons_count": lessons_count,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {exc}")
