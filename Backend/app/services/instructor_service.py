from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models.analytics_summary import AnalyticsSummary
from app.models.assessment import Assessment
from app.models.practice_session import PracticeSession
from app.models.role import Role
from app.models.user import User


class InstructorService:

    @staticmethod
    def get_assigned_students(db: Session):

        students = (
            db.query(User)
            .join(Role, User.role_id == Role.id)
            .filter(func.lower(Role.name) == "learner")
            .all()
        )

        return students

    @staticmethod
    def get_student_progress(
        db: Session,
        student_id,
    ):

        progress = (
            db.query(AnalyticsSummary)
            .filter(
                AnalyticsSummary.user_id == student_id
            )
            .first()
        )

        if progress is None:
            return {
                "average_accuracy": 0.0,
                "lessons_completed": 0,
                "total_practice_time": 0,
                "weak_letters": [],
            }

        return progress

    @staticmethod
    def get_student_assessments(
        db: Session,
        student_id,
    ):

        return (
            db.query(Assessment)
            .join(
                PracticeSession,
                Assessment.session_id == PracticeSession.id,
            )
            .filter(PracticeSession.user_id == student_id)
            .all()
        )
