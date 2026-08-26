from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    ai,
    practice,
    assessment,
    feedback,
    analytics,
    integration,
    streak,
    badge,
    leaderboard,
    progress_report,
    reports,
)

from routers.certificate import router as certificate_router
from routers.recommendation import router as recommendation_router
from routers.weekly_analytics import router as weekly_analytics_router
from routers.certification_exam import router as certification_exam_router
from routers.accessibility_trainer import router as accessibility_trainer_router


app = FastAPI(title="Business Logic Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Deployed Vercel frontend (production + preview deployments)
        "https://sign-language-frontend-two.vercel.app",
        "https://sign-language-frontend-obzwzgebb.vercel.app",
        "https://sign-language-frontend-5csyicbdf.vercel.app",
        "https://sign-language-frontend-kfyiuabiq.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ai.router)
app.include_router(weekly_analytics_router)
app.include_router(practice.router)
app.include_router(assessment.router)
app.include_router(certificate_router)
app.include_router(feedback.router)
app.include_router(analytics.router)
app.include_router(streak.router)
app.include_router(badge.router)
app.include_router(leaderboard.router)
app.include_router(progress_report.router)
app.include_router(reports.router)
app.include_router(integration.router)
app.include_router(recommendation_router)
app.include_router(certification_exam_router)
app.include_router(accessibility_trainer_router)



@app.get("/health")
def health_check():
    return {"status": "ok"}