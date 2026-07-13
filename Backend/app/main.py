from fastapi import FastAPI
from app.routers import auth
from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit

print("******** MY MAIN.PY IS LOADED ********")

# Create FastAPI app FIRST
app = FastAPI(
    title="AI-Powered Sign Language Learning & Assessment Platform",
    description="Backend API for Sign Language Learning & Assessment Platform.",
    version="1.0.0",
)

# Register middleware
app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)

# Register router ONLY ONCE
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "Backend API is running successfully!"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "backend",
        "version": "1.0.0",
    }


print("\n===== Registered Routes =====")
for route in app.routes:
    print(route.path, route.methods)
print("=============================\n")

print("\n===== OpenAPI Paths =====")
print(app.openapi()["paths"].keys())
print("=========================\n")
