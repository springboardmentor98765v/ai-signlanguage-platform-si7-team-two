from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_router import router as user_router

app = FastAPI(
    title="AI-Powered Sign Language Learning & Assessment Platform",
    description="Backend API for Sign Language Learning & Assessment Platform.",
    version="1.0.0",
)

# Allow React frontend to access the backend
origins = [
    "http://localhost:5173",  # Vite React
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint to verify that the backend server is running.
    """
    return {
        "message": "Backend API is running successfully!"
    }


@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint to verify API status.
    """
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0"
    }