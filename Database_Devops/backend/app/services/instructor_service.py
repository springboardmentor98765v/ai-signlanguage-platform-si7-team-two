from sqlalchemy.orm import Session

from db.models.users import User
from db.models.roles import Role
from db.models.practice_sessions import PracticeSession
from db.models.assessments import Assessment
from db.models.learner_analytics import LearnerAnalytics


class InstructorService:

    @staticmethod
    def get_assigned_students(db: Session):

        students = (
            db.query(User)
            .join(Role)
            .filter(Role.name == "Learner")
            .all()
        )

        return students

    @staticmethod
    def get_student_progress(
        db: Session,
        student_id,
    ):

        progress = (
            db.query(LearnerAnalytics)
            .filter(
                LearnerAnalytics.user_id == student_id
            )
            .first()
        )

        if progress is None:
            raise ValueError("Student progress not found")

        return progress

    @staticmethod
    def get_student_assessments(
        db: Session,
        student_id,
    ):

        assessments = (
            db.query(Assessment)
            .join(
                PracticeSession,
                Assessment.session_id == PracticeSession.id,
            )
            .filter(
                PracticeSession.user_id == student_id
            )
            .all()
        )

        return assessments