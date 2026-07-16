"""
db/scripts/smoke_test_orm.py

Goes one step further than verify_orm_models.py's structural check: proves
the ORM models actually work end-to-end against the live Day 2 database —
querying seeded rows, and performing a real insert/query/delete round trip
so a genuine integration bug (not just a column-name mismatch) would be
caught here too.

Usage (run from repo root):
    python -m db.scripts.smoke_test_orm
"""
from db.database import get_session
from db.models import Role, User, Course, Lesson


def run() -> None:
    session = get_session()
    try:
        print("== Reading seeded data (from Day 2's seed.sql) ==")
        roles = session.query(Role).order_by(Role.name).all()
        print(f"Roles found: {[r.name for r in roles]}")
        assert len(roles) == 4, f"expected 4 seeded roles, found {len(roles)}"

        lessons = session.query(Lesson).join(Course).order_by(Lesson.order_index).all()
        print(f"Lessons found: {[(lesson.letter, lesson.course.name) for lesson in lessons]}")
        assert len(lessons) == 5, f"expected 5 seeded lessons, found {len(lessons)}"

        print("\n== Insert/query/delete round trip (proves ORM writes actually work) ==")
        learner_role = session.query(Role).filter_by(name="Learner").one()

        test_user = User(
            full_name="Day 3 Smoke Test User",
            email="day3-smoke-test@example.invalid",
            password_hash="not-a-real-hash-this-is-a-test-row",
            role_id=learner_role.id,
        )
        session.add(test_user)
        session.commit()
        print(f"Inserted test user: {test_user.id}")

        fetched = session.query(User).filter_by(email="day3-smoke-test@example.invalid").one()
        assert fetched.id == test_user.id
        assert fetched.role.name == "Learner"
        print(f"Fetched back successfully, role relationship resolved to: {fetched.role.name}")

        session.delete(fetched)
        session.commit()
        print("Cleaned up test user.")

        print("\nALL SMOKE TESTS PASSED")
    except Exception:
        session.rollback()
        print("\nSMOKE TEST FAILED — rolled back any partial changes.")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
