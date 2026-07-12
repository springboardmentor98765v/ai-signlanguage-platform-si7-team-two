from fastapi import FastAPI
from routers import practice, assessment, feedback

app = FastAPI(title="Business Logic Service")

app.include_router(practice.router)
app.include_router(assessment.router)
app.include_router(feedback.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}