from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.lesson_service import (
    get_all_lessons,
    get_lesson_by_id,
)

router = APIRouter()


@router.get("/")
def list_lessons(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return get_all_lessons(
        db=db,
        page=page,
        limit=limit,
        search=search,
    )


@router.get("/{lesson_id}")
def lesson_details(
    lesson_id: UUID,
    db: Session = Depends(get_db),
):
    lesson = get_lesson_by_id(
        db,
        lesson_id,
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return lesson
