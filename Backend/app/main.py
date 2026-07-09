from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Sign Language Learning & Assessment Platform",
    description="Backend API for Sign Language Learning & Assessment Platform.",
    version="1.0.0",
)


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