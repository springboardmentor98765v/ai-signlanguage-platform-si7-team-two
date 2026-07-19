from sqlalchemy.orm import Session
from sqlalchemy import or_

from db.models.lessons import Lesson


def get_all_lessons(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
):
    """
    Returns lessons with pagination and search.
    """

    query = db.query(Lesson)

    if search:
        query = query.filter(
            or_(
                Lesson.title.ilike(f"%{search}%"),
                Lesson.letter.ilike(f"%{search}%"),
            )
        )

    offset = (page - 1) * limit

    return query.order_by(Lesson.order_index).offset(offset).limit(limit).all()


def get_lesson_by_id(
    db: Session,
    lesson_id,
):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()
