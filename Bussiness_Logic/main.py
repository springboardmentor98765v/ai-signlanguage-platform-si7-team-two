from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai, practice, assessment, feedback, analytics, integration

app = FastAPI(title="Business Logic Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(practice.router)
app.include_router(assessment.router)
app.include_router(feedback.router)
app.include_router(analytics.router)
app.include_router(integration.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
