# AI-Powered Sign Language Learning & Assessment Platform — Milestone 1

Monorepo for the 5-intern Milestone 1 build (see SRS v1.0).

## Repo layout
- `frontend/` — Intern 1 (Application Layer)
- `backend/` — Intern 2 (Auth/Course APIs) & Intern 4 (Practice/Assessment/Feedback/Analytics)
- `ai-service/` — Intern 3 (CV + AI/ML)
- `db/` — Intern 5 (Data Layer): ER diagram, schema, seed data — **start here**
- `infra/` — Intern 5 (Infrastructure Layer): Docker/Compose/CI (added from Day 5)

## Status: Day 4
All 8 tables now have SQLAlchemy models and Alembic migrations —
`db/models/` and `db/migrations/` are complete for the whole schema
(practice sessions, assessments, feedback, and learner analytics added on
top of Day 3's roles/users/courses/lessons). See `db/README.md` for setup
and verification scripts. Full multi-service Docker Compose and CI are
still Day 5/6.

## Setup
Nothing to run yet on Day 1. Once Day 2's database is live, each subproject
will get its own setup instructions in its README.
