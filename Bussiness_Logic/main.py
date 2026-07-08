from fastapi import FastAPI
from routers import practice

app = FastAPI(title="Business Logic Service")

app.include_router(practice.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}