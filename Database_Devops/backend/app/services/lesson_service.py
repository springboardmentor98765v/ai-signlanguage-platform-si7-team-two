from uuid import UUID

from sqlalchemy.orm import Session

from db.models.lessons import Lesson
from app.schemas.lesson_schema import LessonCreate, LessonUpdate


def get_all_lessons(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str = None,
):
    query = db.query(Lesson)

    if search:
        query = query.filter(Lesson.title.ilike(f"%{search}%"))

    return (
        query.order_by(Lesson.order_index).offset((page - 1) * limit).limit(limit).all()
    )


def get_lesson_by_id(
    db: Session,
    lesson_id: UUID,
):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def create_lesson(
    db: Session,
    lesson: LessonCreate,
):
    new_lesson = Lesson(**lesson.model_dump())

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


def update_lesson(
    db: Session,
    lesson_id: UUID,
    lesson: LessonUpdate,
):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if db_lesson is None:
        return None

    for key, value in lesson.model_dump(exclude_unset=True).items():
        setattr(db_lesson, key, value)

    db.commit()
    db.refresh(db_lesson)

    return db_lesson


def delete_lesson(
    db: Session,
    lesson_id: UUID,
):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if db_lesson is None:
        return None

    db.delete(db_lesson)
    db.commit()

    return {"message": "Lesson deleted successfully"}
