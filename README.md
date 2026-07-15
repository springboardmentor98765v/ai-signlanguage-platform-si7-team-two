# AI-Powered Sign Language Learning & Assessment Platform — Milestone 1

Monorepo for the 5-intern Milestone 1 build (see SRS v1.0). This README is
the team setup guide (SRS §6, Intern 5, Day 6 deliverable) — start here.

## Repo layout
- `frontend/` — Intern 1 (Application Layer)
- `backend/` — Intern 2 (Auth/Course APIs) & Intern 4 (Practice/Assessment/Feedback/Analytics). Currently a placeholder app — see `backend/README.md`.
- `ai-service/` — Intern 3 (CV + AI/ML). Currently a placeholder app — see `ai-service/README.md`.
- `db/` — Intern 5 (Data Layer): ER diagram, schema, ORM models, migrations, verification scripts.
- `infra/` — Intern 5 (Infrastructure Layer): Docker Compose, CI.
- `CONTRIBUTING.md` — branching strategy and Git workflow.

## Quick start (full stack, one command)

```bash
git clone <this repo>
cd sign-language-platform
cp .env.example .env          # or use the team-shared .env directly
./db/scripts/start_full_stack.sh     # Linux/macOS
# .\db\scripts\start_full_stack.ps1  # Windows
```

This builds and starts three containers: Postgres (seeded with roles + 5
sample lessons), a placeholder backend on `:8000`, and a placeholder AI
service on `:8001`.

Check it worked:
- `http://localhost:8000/health` and `http://localhost:8000/health/db`
  (the latter proves the backend container can actually query Postgres)
- `http://localhost:8001/health`

## Database only (for local backend/ai-service development outside Docker)

```bash
./db/scripts/start_db.sh             # Linux/macOS
# .\db\scripts\start_db.ps1          # Windows
```
Don't run this at the same time as the full stack — both manage the same
`signlang_postgres` container/volume. See `db/README.md` for details.

## ORM models & migrations

```bash
pip install -r db/requirements.txt
cd db && alembic stamp head    # your DB already has all 8 tables from the Day 2 bootstrap
cd ..
python -m db.scripts.verify_orm_models        # structural check
python -m db.scripts.smoke_test_orm           # roles/users/courses/lessons round trip
python -m db.scripts.smoke_test_full_journey  # full practice→assessment→feedback→analytics chain
```

## Contributing

See `CONTRIBUTING.md` for branching strategy (feature branches →
`integration` → `main`) and commit conventions. CI (`.github/workflows/ci.yml`)
runs automatically on every push/PR: lint, a real migration run against a
throwaway database, the verification/smoke test scripts, and a Docker
build check for both services.

## Status: Milestone 2, Day 1 — Data Layer planning
Milestone 1 (Days 1-7) is complete — see `DEPLOYMENT_NOTE.md`. Milestone 2
has begun: Day 1 is a planning day for the Data Layer, covering 4 new
entities (Certificates, Recommendations, Instructor-Student mapping,
Weekly Analytics). See `db/milestone2/README.md` for the full plan and
sign-off checklist. Nothing is executed against the live database yet —
that's M2 Day 2.

## Documentation index
- `db/milestone2/README.md` — Milestone 2 Data Layer plan (current)
- `DEPLOYMENT_NOTE.md` — Milestone 1 Day 7 status: what's verified vs. still pending
- `db/DATA_MODEL.md` — full data dictionary
- `db/BASE_DOCUMENT_ALIGNMENT.md` — how this schema maps to the fuller
  base architecture document, and what's deliberately deferred past M1
- `db/README.md` — day-by-day Data Layer log (Day 1 through current)
- `infra/README.md` — Infrastructure Layer log
- `CONTRIBUTING.md` — Git workflow
