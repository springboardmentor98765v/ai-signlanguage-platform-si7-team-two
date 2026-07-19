from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models.users import User
from db.models.learner_analytics import LearnerAnalytics
from db.models.assessments import Assessment


class InstructorService:

    @staticmethod
    def get_assigned_students(db: Session):

        students = db.execute(
            select(User)
        ).scalars().all()

        return students

    @staticmethod
    def get_student_progress(
        db: Session,
        student_id,
    ):

        progress = db.execute(
            select(LearnerAnalytics).where(
                LearnerAnalytics.user_id == student_id
            )
        ).scalar_one_or_none()

        if progress is None:
            raise ValueError("Student progress not found")

        return progress

    @staticmethod
    def get_student_assessments(
        db: Session,
        student_id,
    ):

        assessments = db.execute(
            select(Assessment).where(
                Assessment.user_id == student_id
            )
        ).scalars().all()

        return assessments