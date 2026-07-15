from sqlalchemy.orm import Session
from db.models.lessons import Lesson


def get_all_lessons(db: Session):
    """
    Returns all seeded lessons ordered by order_index.
    """
    return (
        db.query(Lesson).all()
    )


def get_lesson_by_id(db: Session, lesson_id):
    """
    Returns a single lesson.
    """
    return (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )