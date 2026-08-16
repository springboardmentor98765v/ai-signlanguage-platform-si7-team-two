from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Health"]
)


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "sign-language-ai",
        "model": "best_xgb_tuned"
    }