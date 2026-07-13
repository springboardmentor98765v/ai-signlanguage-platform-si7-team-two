# AI-Powered Sign Language Learning & Assessment Platform — Milestone 1

Monorepo for the 5-intern Milestone 1 build (see SRS v1.0).

## Repo layout
- `frontend/` — Intern 1 (Application Layer)
- `Bussiness_Logic/` — Intern 2 (Auth/Course APIs) & Intern 4 (Practice/Assessment/Feedback/Analytics); placeholder FastAPI app + Dockerfile added Day 5
- `AIML_CV/` — Intern 3 (CV + AI/ML); placeholder FastAPI app + Dockerfile added Day 5
- `Database_Devops/db/` — Intern 5 (Data Layer): ER diagram, schema, ORM models, Alembic migrations, seed data, verification & smoke-test scripts — **start here**
- `Database_Devops/infra/` — Intern 5 (Infrastructure Layer): DB-only Compose (Day 2) + full-stack Compose (Day 5)
- `.github/workflows/ci.yml` — Intern 5 (CI): lint + migrate + smoke-test + docker-build (Day 6)

## Status: Day 7 ✅
All Intern 5 deliverables for Milestone 1 are complete:

| Day | Deliverable | Status |
|-----|-------------|--------|
| 1 | ER diagram, data model, schema DDL draft | ✅ Done |
| 2 | Live Postgres instance (Docker), seed data | ✅ Done |
| 3 | SQLAlchemy ORM models for Roles/Users/Courses/Lessons + Alembic | ✅ Done |
| 4 | ORM models for Practice Sessions/Assessments/Feedback/Analytics | ✅ Done |
| 5 | Full-stack Docker Compose (db + Bussiness_Logic + AIML_CV), placeholder services + Dockerfiles | ✅ Done |
| 6 | GitHub Actions CI (lint + real migration + smoke tests + Docker builds) | ✅ Done |
| 7 | Integration check script + deployment note | ✅ Done |

## Quick Start (from repo root)
```bash
# Copy env file
cp .env.example .env

# Start the full stack (db + backend + ai-service)
./Database_Devops/db/scripts/start_full_stack.sh      # Linux/macOS
.\Database_Devops\db\scripts\start_full_stack.ps1     # Windows

# Verify everything
./Database_Devops/db/scripts/integration_check.sh     # Linux/macOS
.\Database_Devops\db\scripts\integration_check.ps1    # Windows
```

See `Database_Devops/db/README.md` for full day-by-day setup, migration, and verification docs.
