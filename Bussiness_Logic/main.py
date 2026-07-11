from fastapi import FastAPI
from routers import practice, assessment

app = FastAPI(title="Business Logic Service")

app.include_router(practice.router)
app.include_router(assessment.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}