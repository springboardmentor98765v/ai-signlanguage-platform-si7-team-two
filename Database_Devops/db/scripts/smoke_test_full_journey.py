"""
db/scripts/smoke_test_full_journey.py

Day 4 functional verification. Exercises the full chain that Day 4 added —
practice_sessions -> assessments -> feedback -> learner_analytics — against
the real, running database, proving relationships resolve correctly end to
end (not just that column names match). Mirrors the "learner practices a
sign, gets scored, gets feedback, analytics updates" journey described in
the base architecture document.

Cleans up everything it creates. Safe to run repeatedly.

Usage (run from repo root):
    python -m db.scripts.smoke_test_full_journey
"""
from decimal import Decimal

from db.database import get_session
from db.models import Role, User, Lesson, PracticeSession, Assessment, Feedback, LearnerAnalytics


def run() -> None:
    session = get_session()
    try:
        print("== Setting up: fetch an existing seeded role + lesson ==")
        learner_role = session.query(Role).filter_by(name="Learner").one()
        lesson_a = session.query(Lesson).filter_by(letter="A").one()
        print(f"Using role={learner_role.name}, lesson={lesson_a.letter} ({lesson_a.id})")

        print("\n== Step 1: create a test learner ==")
        test_user = User(
            full_name="Day 4 Smoke Test Learner",
            email="day4-smoke-test@example.invalid",
            password_hash="not-a-real-hash-this-is-a-test-row",
            role_id=learner_role.id,
        )
        session.add(test_user)
        session.flush()  # get test_user.id without a full commit yet
        print(f"Created user: {test_user.id}")

        print("\n== Step 2: start a practice session for Lesson A ==")
        practice_session = PracticeSession(
            user_id=test_user.id,
            lesson_id=lesson_a.id,
            status="completed",
            attempt_count=2,
        )
        session.add(practice_session)
        session.flush()
        print(f"Created practice_session: {practice_session.id}")

        print("\n== Step 3: record an AI assessment for that session ==")
        assessment = Assessment(
            session_id=practice_session.id,
            predicted_sign="A",
            confidence=Decimal("0.9640"),
            expected_sign="A",
            accuracy_score=Decimal("90.00"),
        )
        session.add(assessment)
        session.flush()
        print(f"Created assessment: {assessment.id} (accuracy={assessment.accuracy_score})")

        print("\n== Step 4: attach rule-based feedback to that assessment ==")
        feedback_row = Feedback(
            assessment_id=assessment.id,
            category="hand_shape",
            message="Keep your thumb closer to the palm.",
        )
        session.add(feedback_row)
        session.flush()
        print(f"Created feedback: {feedback_row.id}")

        print("\n== Step 5: upsert learner_analytics for this user ==")
        analytics = LearnerAnalytics(
            user_id=test_user.id,
            average_accuracy=Decimal("90.00"),
            lessons_completed=1,
            weak_letters=[],
        )
        session.add(analytics)
        session.commit()
        print(f"Created learner_analytics: {analytics.id}")

        print("\n== Verifying relationships resolve correctly from a fresh query ==")
        fetched_user = session.query(User).filter_by(email="day4-smoke-test@example.invalid").one()
        assert len(fetched_user.practice_sessions) == 1
        fetched_session = fetched_user.practice_sessions[0]
        assert len(fetched_session.assessments) == 1
        fetched_assessment = fetched_session.assessments[0]
        assert len(fetched_assessment.feedback_items) == 1
        assert fetched_user.analytics.lessons_completed == 1
        print("All relationships resolved correctly: User -> PracticeSession -> Assessment -> Feedback, and User -> LearnerAnalytics")

        print("\n== Cleaning up test data ==")
        session.delete(fetched_user)  # cascades to session/assessment/feedback/analytics
        session.commit()
        print("Cleaned up test user and all cascaded rows.")

        print("\nALL DAY 4 SMOKE TESTS PASSED")
    except Exception:
        session.rollback()
        print("\nSMOKE TEST FAILED — rolled back any partial changes.")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
