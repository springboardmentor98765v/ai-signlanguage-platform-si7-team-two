from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth
from app.routers import practice
from app.routers import lesson
from app.routers import assessment
from app.routers import instructor
from app.routers import trainer
from app.routers import admin
from app.routers import certificate
from app.routers import progress_report
from app.routers import notification

from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit


# Create FastAPI app FIRST
app = FastAPI(
    title="AI-Powered Sign Language Learning & Assessment Platform",
    description="Backend API for Sign Language Learning & Assessment Platform.",
    version="1.0.0",
)


# Register middleware
app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    assessment.router,
    prefix="/assessment",
    tags=["Assessment"],
)

app.include_router(
    practice.router,
    prefix="/ai",
    tags=["AI"],
)

app.include_router(
    lesson.router,
    prefix="/lessons",
    tags=["Lessons"],
)

app.include_router(
    certificate.router,
    prefix="/certificate",
    tags=["Certificate"],
)

app.include_router(
    notification.router,
    prefix="/notifications",
    tags=["Notifications"],
)

app.include_router(
    progress_report.router,
    prefix="/progress-report",
    tags=["Progress Report"],
)

app.include_router(
    instructor.router,
    prefix="/instructor",
    tags=["Instructor"],
)

# Milestone 4 - Day 2: Trainer Dashboard APIs
app.include_router(
    trainer.router,
    prefix="/trainer",
    tags=["Trainer"],
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Backend API is running successfully!"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0",
    }