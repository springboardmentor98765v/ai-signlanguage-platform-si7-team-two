# Data Layer — Day 1 Deliverable

Owner: Intern 5. Task per SRS §6 (Intern 5, Day 1): draft an ER diagram
covering Users/Roles, Lessons/Modules, Practice Sessions, Assessments,
Feedback and Analytics records, for team review.

## Contents
- `erd/erd.mmd` — Mermaid ER diagram (render on GitHub, or paste into
  https://mermaid.live for a visual).
- `DATA_MODEL.md` — plain-English data dictionary: every entity, every
  field, every relationship, with the SRS section that justifies it.
- `BASE_DOCUMENT_ALIGNMENT.md` — maps this schema against the fuller
  base architecture document, and explains every deliberate simplification
  for Milestone 1 (5 conceptual databases → 1 shared DB, deferred
  sub-scores, deferred advanced analytics, etc). Read this before a
  mentor review if anything looks like it's "missing" compared to the
  base doc's diagram.
- `schema/schema.sql` — the ERD translated into PostgreSQL DDL. **Draft
  only** — not executed against any database yet. This exists so Intern 2
  and Intern 4 can start writing ORM models/Pydantic schemas against real
  column names as soon as the ERD is approved, without waiting for Day 2's
  live instance.
- `schema/seed.sql` — draft seed data (roles, alphabet lessons A/B/C/L/Y
  matching Intern 3's SRS Day 4 sample letters). **Not run yet** — real
  seeding happens Day 5 (SRS §6, Intern 2 Day 5) once the schema is final
  and a live DB exists (Day 2).

## Review checklist for Interns 2 & 4 (please confirm by end of Day 1)
- [ ] Does `users`/`roles` support the RBAC roles needed for FR-2
      (Learner/Instructor/Trainer/Admin)?
- [ ] Does `assessments` carry the exact fields Intern 3's prediction
      service will return (`predicted_sign`, `confidence`) per FR-3?
- [ ] Does `practice_sessions` capture what Intern 4's scoring engine
      needs (attempt count, duration, status) per FR-4?
- [ ] Any missing fields for the Frontend's mock-to-real API swap (Day 6)?

Sign-off here unblocks Day 2 (live Postgres instance) and Day 3-4 (ORM
models), per the Dependency Matrix in SRS §5.

---

## Day 2 — Live Database (SRS §6, Intern 5, Day 2)

**Status: done.** The reviewed schema above is now running.

### Start it (run from repo root)
```bash
cp .env.example .env   # or use the shared .env from Intern 5 directly
./db/scripts/start_db.sh          # Linux/macOS
.\db\scripts\start_db.ps1         # Windows PowerShell
```
This starts a single Postgres 16 container, waits for its healthcheck, and
— on first run only — automatically applies `infra/init/01-schema.sql` and
`infra/init/02-seed.sql` (copies of the files in `db/schema/`).

### Verify it worked
```bash
./db/scripts/verify_connection.sh    # Linux/macOS
.\db\scripts\verify_connection.ps1   # Windows PowerShell
```
Expect to see all 8 tables, 4 seeded roles, and 5 seeded lessons (A, B, C, L, Y).

### If the schema changes after review feedback
Postgres only auto-applies `infra/init/*.sql` the very first time (on an
empty data volume). If Intern 2 or Intern 4 request a schema change:
1. Edit `db/schema/schema.sql` (source of truth) and the matching copy in
   `infra/init/01-schema.sql`.
2. Re-apply cleanly:
   ```bash
   ./db/scripts/reset_db.sh     # Linux/macOS — wipes and recreates
   .\db\scripts\reset_db.ps1    # Windows
   ```

### Credentials (SRS Day 2 deliverable: "share connection details/credentials")
Local dev credentials live in the repo-root `.env` (gitignored — copy it
directly to Intern 2 and Intern 4, don't push it to Git). Connection string
format: `DATABASE_URL` in that file.

### Note on "base tables vs full tables" (SRS §5 Dependency Matrix)
The matrix lists base tables by end of Day 2 and full tables by Day 4. All
8 tables from the Day 1-reviewed ERD are created now, since the design was
already approved as one unit — see the assumption noted in the Part 1
summary. Day 3/4 remain responsible for writing the actual SQLAlchemy ORM
models and verifying each table group against their services; the tables
themselves simply already exist to build against.

---

## Day 3 — ORM Models & Migrations (SRS §6, Intern 5, Day 3)

**Scope: Roles, Users, Courses, Lessons only** — Practice Sessions,
Assessments, Feedback, and Learner Analytics models are Day 4.

### What's here
- `models/` — SQLAlchemy 2.0-style ORM classes (`Role`, `User`, `Course`,
  `Lesson`), one file each, mirroring `schema/schema.sql` exactly.
- `database.py` — the single place the SQLAlchemy engine/session are
  configured, reading `DATABASE_URL` from the repo-root `.env`. Intern 2's
  FastAPI app should import `get_session` from here rather than creating
  its own engine.
- `migrations/` — an Alembic project. This formalizes schema changes as
  versioned migrations going forward, instead of hand-editing
  `schema.sql`/`infra/init/*.sql` as Day 1/2 did to move fast early on.
- `requirements.txt` — `sqlalchemy`, `alembic`, `psycopg2-binary`,
  `python-dotenv`.

### Setup
```bash
pip install -r db/requirements.txt
```

### Important: your database already has these tables (from Day 2)
Day 2 created all 8 tables via Docker's one-time init-script bootstrap —
not via Alembic. So on your existing Day 2 database, do **not** run
`alembic upgrade head` (it will fail with "relation already exists").
Instead, tell Alembic the database is already at this migration:
```bash
cd db
alembic stamp head
```
From this point forward, make schema changes as new Alembic migrations
(`alembic revision --autogenerate -m "..."`), not by hand-editing
`schema.sql` directly.

For a genuinely fresh/empty database (e.g. a new teammate's local Postgres
with no init-script bootstrap, or CI), `alembic upgrade head` runs the real
DDL from scratch.

### Verification
Two scripts, run from the repo root:
```bash
python -m db.scripts.verify_orm_models   # structural: ORM columns vs live DB columns
python -m db.scripts.smoke_test_orm      # functional: real insert/query/delete round trip
```
`verify_orm_models.py` checks every column the 4 Day 3 models declare
actually exists on the live table with matching nullability.
`smoke_test_orm.py` queries the Day 2 seed data (4 roles, 5 lessons) and
performs a real insert → query → delete of a test user, proving the ORM
relationships (e.g. `user.role.name`) actually resolve against real data.

**Scope honesty:** the SRS's actual Day 3 instruction is to *"verify with
Intern 2's User/Course Service"* — a teammate's FastAPI service, which
doesn't exist in this solo engagement. These two scripts are the closest
solo equivalent (proving the models are structurally and functionally
correct against the live DB). The real cross-service check against Intern
2's actual API still needs to happen once that service exists.
