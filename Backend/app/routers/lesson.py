from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import require_learner
from app.schemas.lesson_schema import LessonCreate, LessonUpdate, LessonWithProgress, LessonCompleteRequest
from app.services.lesson_service import (
    get_all_lessons,
    get_lesson_by_id,
    create_lesson,
    update_lesson,
    delete_lesson,
    get_lessons_with_progress,
    complete_lesson
)

router = APIRouter()


@router.get("/")
def list_lessons(
    page: int = 1,
    limit: int = 100,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return get_all_lessons(
        db=db,
        page=page,
        limit=limit,
        search=search,
    )

@router.get("/with-progress/{user_id}", response_model=List[LessonWithProgress])
def list_lessons_with_progress(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """Returns lessons augmented with progression data (stars, accuracy, locked status)."""
    return get_lessons_with_progress(db, user_id)

@router.post("/{lesson_id}/complete/{user_id}")
def mark_lesson_complete(
    lesson_id: UUID,
    user_id: UUID,
    req: LessonCompleteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_learner),
):
    """Mark lesson completed, calculate stars, update highest accuracy, unlock next."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only complete lessons for your own account",
        )
    return complete_lesson(db, user_id, lesson_id, req.accuracy)

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
