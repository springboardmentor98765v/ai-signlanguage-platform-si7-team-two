# Backend (Intern 2 & Intern 4)

Placeholder — FastAPI project scaffolding begins Day 2 (Intern 2). As of
Day 4, ALL ORM models are ready at `db/models/` (import via
`from db.models import Role, User, Course, Lesson, PracticeSession,
Assessment, Feedback, LearnerAnalytics`) and the engine/session factory is
at `db/database.py` (`get_session()`). Build your FastAPI routers against
these rather than defining your own models, to avoid drift from the
reviewed schema. Intern 4: `PracticeSession.assessments`,
`Assessment.feedback_items`, and `User.analytics` relationships are already
wired for you.
