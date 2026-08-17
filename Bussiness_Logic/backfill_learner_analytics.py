from database import SessionLocal
from models.practice_model import PracticeSession
from services.learner_analytics_service import refresh_learner_analytics


def main():
    db = SessionLocal()

    try:
        user_ids = (
            db.query(PracticeSession.user_id)
            .distinct()
            .all()
        )

        print(f"Found {len(user_ids)} learners with practice history.")

        for (user_id,) in user_ids:
            refresh_learner_analytics(
                db,
                user_id,
            )

            print(
                f"Analytics refreshed for learner: {user_id}"
            )

        print("\nBackfill completed successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()