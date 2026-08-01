from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.lesson_schema import LessonCreate, LessonUpdate
from app.services.lesson_service import (
    get_all_lessons,
    get_lesson_by_id,
    create_lesson,
    update_lesson,
    delete_lesson,
)

router = APIRouter()


@router.get("/")
def list_lessons(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    db: Session =Depends(get_db),
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
    lesson = get_lesson_by_id(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return lesson


@router.post("/")
def add_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
):
    return create_lesson(db, lesson)


@router.put("/{lesson_id}")
def edit_lesson(
    lesson_id: UUID,
    lesson: LessonUpdate,
    db: Session = Depends(get_db),
):
    updated = update_lesson(
        db,
        lesson_id,
        lesson,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return updated


@router.delete("/{lesson_id}")
def remove_lesson(
    lesson_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = delete_lesson(
        db,
        lesson_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return {
        "message": "Lesson deleted successfully"
    }