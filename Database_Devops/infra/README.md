# Infrastructure (Intern 5 — Database & DevOps)

## Day 2 ✅
`docker-compose.db.yml` + `init/` — stands up the shared Postgres instance
only. Useful when developing backend/ai-service locally (outside Docker)
against a containerized DB.

## Day 5 ✅
`docker-compose.yml` — the full stack: db + backend + ai-service together,
one command. `backend/Dockerfile` and `ai-service/Dockerfile` build
placeholder services since Intern 2/3's real code lives in their own
track branches.

**Note:** `docker-compose.db.yml` and `docker-compose.yml` both manage a
container named `signlang_postgres` — don't run both at once. Use
`db/scripts/start_full_stack.sh` (or `.ps1`), which stops the db-only one
automatically before starting the full stack.

## Day 7 ✅ (Milestone 2)
`docker-compose.yml` updated:
- `backend` now mounts the shared `certificates_data` volume at
  `/app/generated_certificates` (for Intern 4's PDF certificates).
- `backend` and `ai-service` both load the full `.env` file, which includes
  the new email variables (`EMAIL_HOST`, `EMAIL_PORT`, …) for Intern 2's
  forgot-password flow.
- `certificates_data` added to the top-level `volumes:` block.

`.env.example` updated with all Milestone 2 variables (see project root).

## Related Milestone 2 deliverables
- **Day 6** — backup/restore system → `../backup/`
- **Day 8** — uptime monitoring + load test → `../monitoring/`
