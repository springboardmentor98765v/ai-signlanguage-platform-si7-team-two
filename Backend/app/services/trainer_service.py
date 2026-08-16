from uuid import UUID
from statistics import mean

from sqlalchemy.orm import Session

from app.models.analytics_summary import AnalyticsSummary
from app.models.assessment import Assessment
from app.models.certificate import Certificate
from app.models.lesson import Lesson
from app.models.practice_session import PracticeSession
from app.models.role import Role
from app.models.streak import Streak
from app.models.user import User


WEAK_LETTER_THRESHOLD = 70.0


class TrainerService:

    @staticmethod
    def get_assigned_learners(db: Session):

        learners = (
            db.query(User)
            .join(Role)
            .filter(Role.name == "Learner")
            .all()
        )

        return [
            {
                "id": learner.id,
                "full_name": learner.full_name,
                "email": learner.email,
                "relationship": "Trainer-Learner",
            }
            for learner in learners
        ]

    @staticmethod
    def _get_assessments(db: Session, learner_id: UUID):

        return (
            db.query(Assessment)
            .join(
                PracticeSession,
                Assessment.session_id == PracticeSession.id,
            )
            .filter(
                PracticeSession.user_id == learner_id
            )
            .order_by(Assessment.created_at.asc())
            .all()
        )

    @staticmethod
    def _get_practice_sessions(db: Session, learner_id: UUID):

        return (
            db.query(PracticeSession)
            .filter(
                PracticeSession.user_id == learner_id
            )
            .all()
        )

    @staticmethod
    def get_learner_engagement(
        db: Session,
        learner_id: UUID,
    ):

        sessions = TrainerService._get_practice_sessions(
            db,
            learner_id,
        )

        total_sessions = len(sessions)

        completed_sessions = sum(
            1
            for session in sessions
            if session.status == "completed"
        )

        total_attempts = sum(
            session.attempt_count or 0
            for session in sessions
        )

        analytics = (
            db.query(AnalyticsSummary)
            .filter(
                AnalyticsSummary.user_id == learner_id
            )
            .first()
        )

        streak = (
            db.query(Streak)
            .filter(
                Streak.learner_id == learner_id
            )
            .first()
        )

        return {
            "total_practice_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "total_attempts": total_attempts,
            "total_practice_time": (
                analytics.total_practice_time
                if analytics
                else 0
            ),
            "current_streak": (
                streak.current_streak
                if streak
                else 0
            ),
            "longest_streak": (
                streak.longest_streak
                if streak
                else 0
            ),
        }

    @staticmethod
    def get_learner_skill_development(
        db: Session,
        learner_id: UUID,
    ):

        assessments = TrainerService._get_assessments(
            db,
            learner_id,
        )

        scores = [
            float(assessment.overall_score)
            for assessment in assessments
        ]

        if scores:
            overall_average = mean(scores)
        else:
            overall_average = 0.0

        if len(scores) <= 1:
            previous_scores = []
            recent_scores = scores
        else:
            split_index = len(scores) // 2

            previous_scores = scores[:split_index]
            recent_scores = scores[split_index:]

        previous_average = (
            mean(previous_scores)
            if previous_scores
            else 0.0
        )

        recent_average = (
            mean(recent_scores)
            if recent_scores
            else 0.0
        )

        improvement = recent_average - previous_average

        letter_scores = {}

        for assessment in assessments:

            letter = assessment.expected_sign.upper()

            letter_scores.setdefault(
                letter,
                [],
            ).append(
                float(assessment.overall_score)
            )

        weak_letters = sorted(
            letter
            for letter, letter_score_list
            in letter_scores.items()
            if mean(letter_score_list) < WEAK_LETTER_THRESHOLD
        )

        return {
            "overall_average_accuracy": round(
                overall_average,
                2,
            ),
            "recent_average_accuracy": round(
                recent_average,
                2,
            ),
            "previous_average_accuracy": round(
                previous_average,
                2,
            ),
            "weak_letters": weak_letters,
            "improvement": round(
                improvement,
                2,
            ),
        }

    @staticmethod
    def get_learner_assessment_analytics(
        db: Session,
        learner_id: UUID,
    ):

        assessments = TrainerService._get_assessments(
            db,
            learner_id,
        )

        if not assessments:

            return {
                "total_assessments": 0,
                "average_assessment_score": 0.0,
                "highest_score": 0.0,
                "lowest_score": 0.0,
                "attempted_letters": [],
                "weak_letters": [],
            }

        scores = [
            float(assessment.overall_score)
            for assessment in assessments
        ]

        attempted_letters = sorted(
            {
                assessment.expected_sign.upper()
                for assessment in assessments
            }
        )

        letter_scores = {}

        for assessment in assessments:

            letter = assessment.expected_sign.upper()

            letter_scores.setdefault(
                letter,
                [],
            ).append(
                float(assessment.overall_score)
            )

        weak_letters = sorted(
            letter
            for letter, letter_score_list
            in letter_scores.items()
            if mean(letter_score_list) < WEAK_LETTER_THRESHOLD
        )

        return {
            "total_assessments": len(assessments),
            "average_assessment_score": round(
                mean(scores),
                2,
            ),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "attempted_letters": attempted_letters,
            "weak_letters": weak_letters,
        }

    @staticmethod
    def get_learner_certification_status(
        db: Session,
        learner_id: UUID,
    ):

        sessions = TrainerService._get_practice_sessions(
            db,
            learner_id,
        )

        assessments = TrainerService._get_assessments(
            db,
            learner_id,
        )

        # Letters attempted through practice sessions
        attempted_letters = sorted(
            {
                session.lesson.letter.upper()
                for session in sessions
                if session.lesson is not None
                and session.lesson.letter
            }
        )

        # Letters completed through completed practice sessions
        completed_letters = sorted(
            {
                session.lesson.letter.upper()
                for session in sessions
                if session.status == "completed"
                and session.lesson is not None
                and session.lesson.letter
            }
        )

        # All available lesson letters
        all_letters = sorted(
            {
                lesson.letter.upper()
                for lesson in db.query(Lesson).all()
                if lesson.letter
            }
        )

        missing_letters = sorted(
            set(all_letters) - set(attempted_letters)
        )

        certificate = (
            db.query(Certificate)
            .filter(
                Certificate.learner_id == learner_id,
                Certificate.is_valid == True,
            )
            .order_by(
                Certificate.issued_at.desc()
            )
            .first()
        )

        scores = [
            float(assessment.overall_score)
            for assessment in assessments
        ]

        overall_average = (
            mean(scores)
            if scores
            else 0.0
        )

        if certificate:

            average_score = float(
                certificate.average_score
            )

            certificate_details = {
                "certificate_code": certificate.certificate_code,
                "issued_at": certificate.issued_at,
                "file_path": certificate.file_path,
                "is_valid": certificate.is_valid,
            }

            return {
                "certification_status": "Certified",
                "average_score": round(
                    average_score,
                    2,
                ),
                "attempted_letters": attempted_letters,
                "completed_letters": completed_letters,
                "missing_letters": missing_letters,
                "certificate_earned": True,
                "certificate_details": certificate_details,
            }

        return {
            "certification_status": "Not certified",
            "average_score": round(
                overall_average,
                2,
            ),
            "attempted_letters": attempted_letters,
            "completed_letters": completed_letters,
            "missing_letters": missing_letters,
            "certificate_earned": False,
            "certificate_details": None,
        }
