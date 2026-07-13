from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.prediction import router as prediction_router
from fastapi.middleware.cors import CORSMiddleware
from api.exceptions import (
    AIServiceException,
    ai_exception_handler
)

app = FastAPI(
    title="Sign Language Assessment API",
    version="1.0.0",
    description="AI Microservice for Sign Language Recognition"
)
# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React Development
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Register Global Exception Handler
# --------------------------------------------------

app.add_exception_handler(
    AIServiceException,
    ai_exception_handler
)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------
@app.get(
    "/",
    tags=["Home"],
    summary="API Information"
)
def home():
    return {
        "service": "Sign Language Recognition AI Service",
        "version": "1.0.0",
        "status": "Running"
    }

# --------------------------------------------------
# Include Routers
# --------------------------------------------------

app.include_router(health_router)
app.include_router(prediction_router)