# Infrastructure (Intern 5)

## Day 2 (done)
`docker-compose.db.yml` + `init/` — stands up the shared Postgres instance
only. Useful when developing backend/ai-service locally (outside Docker)
against a containerized DB.

## Day 5 (done)
`docker-compose.yml` — the full stack: db + backend + ai-service together,
one command. `backend/Dockerfile` and `ai-service/Dockerfile` build
placeholder services (see their `app/main.py` files) since Intern 2/3's
real code doesn't exist in this solo build yet.

**Note:** `docker-compose.db.yml` and `docker-compose.yml` both manage a
container named `signlang_postgres` — don't run both at once. Use
`db/scripts/start_full_stack.sh` (or `.ps1`), which stops the db-only one
automatically before starting the full stack.

## Still to come
- `.github/workflows/ci.yml` CI stub (Day 6, SRS §6)
