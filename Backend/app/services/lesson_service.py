import logging
from datetime import datetime, timezone
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress
from app.schemas.lesson_schema import LessonCreate, LessonUpdate, LessonWithProgress
from app.services.analytics_service import update_analytics_summary


logger = logging.getLogger(__name__)

def get_all_lessons(
    db: Session,
    page: int = 1,
    limit: int = 100,
    search: str = None,
):
    query = db.query(Lesson)
    if search:
        query = query.filter(Lesson.title.ilike(f"%{search}%"))
    return query.order_by(Lesson.order_index).offset((page - 1) * limit).limit(limit).all()

def get_lesson_by_id(db: Session, lesson_id: UUID):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()

def get_lessons_with_progress(db: Session, user_id: UUID) -> List[dict]:
    """Returns lessons augmented with progress (status, stars, accuracy) for a given user."""
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    progress_records = db.query(LessonProgress).filter(LessonProgress.user_id == user_id).all()
    progress_map = {p.lesson_id: p for p in progress_records}
    
    result = []
    # By default, first lesson is unlocked, others are locked until previous is completed.
    # We'll determine status linearly.
    is_next_unlocked = True
    
    for idx, lesson in enumerate(lessons):
        progress = progress_map.get(lesson.id)
        
        lesson_data = {
            "id": str(lesson.id),
            "course_id": str(lesson.course_id),
            "letter": lesson.letter,
            "title": lesson.title,
            "description": lesson.description,
            "reference_image_url": lesson.reference_image_url,
            "order_index": lesson.order_index,
            "stars": 0,
            "accuracy": 0.0,
            "status": "locked"
        }
        
        if progress:
            lesson_data["stars"] = progress.stars
            lesson_data["accuracy"] = float(progress.highest_accuracy)
            if progress.is_completed:
                lesson_data["status"] = "completed"
                is_next_unlocked = True
            elif progress.is_unlocked:
                lesson_data["status"] = "current"
                # if current is not completed, next one is locked
                is_next_unlocked = False
        else:
            if is_next_unlocked:
                lesson_data["status"] = "current"
                is_next_unlocked = False
            else:
                lesson_data["status"] = "locked"
                
        result.append(lesson_data)
        
    return result

def complete_lesson(db: Session, user_id: UUID, lesson_id: UUID, accuracy: float) -> dict:
    """Marks a lesson as completed, calculates stars based on accuracy, updates progress."""
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            is_unlocked=True
        )
        db.add(progress)
        
    # Calculate stars: 90%+ = 3 stars, 75%+ = 2 stars, 60%+ = 1 star, else 0
    stars = 0
    if accuracy >= 90:
        stars = 3
    elif accuracy >= 75:
        stars = 2
    elif accuracy >= 60:
        stars = 1
        
    # Only update if it's a new high score
    if accuracy > float(progress.highest_accuracy):
        progress.highest_accuracy = accuracy
    if stars > progress.stars:
        progress.stars = stars
        
    newly_completed = not progress.is_completed
    progress.is_completed = True
    if progress.completed_at is None:
        progress.completed_at = datetime.now(timezone.utc)

    summary = update_analytics_summary(
        db,
        user_id,
        accuracy,
        lesson_completed=newly_completed,
    )
    
    # Unlock the next lesson
    current_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if current_lesson:
        next_lesson = db.query(Lesson).filter(Lesson.order_index > current_lesson.order_index).order_by(Lesson.order_index).first()
        if next_lesson:
            next_progress = db.query(LessonProgress).filter(
                LessonProgress.user_id == user_id,
                LessonProgress.lesson_id == next_lesson.id
            ).first()
            
            if not next_progress:
                next_progress = LessonProgress(
                    user_id=user_id,
                    lesson_id=next_lesson.id,
                    is_unlocked=True
                )
                db.add(next_progress)
            else:
                next_progress.is_unlocked = True
                
    db.commit()
    db.refresh(progress)
    db.refresh(summary)

    logger.info(
        "analytics_summary updated: user_id=%s lesson_id=%s accuracy=%s "
        "lessons_completed=%s average_accuracy=%s",
        user_id,
        lesson_id,
        accuracy,
        summary.lessons_completed,
        summary.average_accuracy,
    )
            
    return {
        "message": "Lesson completed",
        "stars": progress.stars,
        "accuracy": float(progress.highest_accuracy)
    }

def create_lesson(db: Session, lesson: LessonCreate):
    new_lesson = Lesson(**lesson.model_dump())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

def update_lesson(db: Session, lesson_id: UUID, lesson: LessonUpdate):
    db_lesson = get_lesson_by_id(db, lesson_id)
    if db_lesson is None:
        return None
    for key, value in lesson.model_dump(exclude_unset=True).items():
        setattr(db_lesson, key, value)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def delete_lesson(db: Session, lesson_id: UUID):
    db_lesson = get_lesson_by_id(db, lesson_id)
    if db_lesson is None:
        return None
    db.delete(db_lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}
