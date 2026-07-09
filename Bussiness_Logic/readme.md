# Backend (Intern 2 & Intern 4)

Placeholder — FastAPI project scaffolding begins Day 2 (Intern 2). As of
Day 3, ORM models for Users/Roles/Courses/Lessons are ready at
`db/models/` (import via `from db.models import Role, User, Course,
Lesson`) and the engine/session factory is at `db/database.py`
(`get_session()`). Build your FastAPI routers against these rather than
defining your own models, to avoid drift from the reviewed schema.
