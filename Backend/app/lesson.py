from fastapi import APIRouter

router = APIRouter()

@router.get("/lessons")
def get_lessons():