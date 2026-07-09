# AI-Powered Sign Language Learning & Assessment Platform — Milestone 1

Monorepo for the 5-intern Milestone 1 build (see SRS v1.0).

## Repo layout
- `frontend/` — Intern 1 (Application Layer)
- `backend/` — Intern 2 (Auth/Course APIs) & Intern 4 (Practice/Assessment/Feedback/Analytics)
- `ai-service/` — Intern 3 (CV + AI/ML)
- `db/` — Intern 5 (Data Layer): ER diagram, schema, seed data — **start here**
- `infra/` — Intern 5 (Infrastructure Layer): Docker/Compose/CI (added from Day 5)

## Status: Day 3
SQLAlchemy ORM models + Alembic migrations added for the Day 3 scope
(roles, users, courses, lessons) in `db/models/` and `db/migrations/`. See
`db/README.md` for setup, the important note about your existing Day 2
database, and verification scripts. Practice Sessions/Assessments/
Feedback/Analytics models remain Day 4. Full multi-service Docker Compose
and CI are still Day 5/6.

## Setup
Nothing to run yet on Day 1. Once Day 2's database is live, each subproject
will get its own setup instructions in its README.
