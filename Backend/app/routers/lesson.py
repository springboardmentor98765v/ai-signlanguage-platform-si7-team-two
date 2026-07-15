from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.lesson_service import get_all_lessons

router = APIRouter()


@router.get("/")
def list_lessons(db: Session = Depends(get_db)):
    return get_all_lessons(db)