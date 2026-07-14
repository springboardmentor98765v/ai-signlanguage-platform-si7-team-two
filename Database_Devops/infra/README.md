# Infrastructure (Intern 5)

## Day 2 (done)
`docker-compose.db.yml` + `init/` — stands up the shared Postgres instance
only. See `db/README.md` for start/verify/reset commands.

## Still to come
- `Dockerfile.backend`, `Dockerfile.ai-service` (Day 5, SRS §6)
- `docker-compose.yml` — the FULL stack (backend + ai-service + db
  together) (Day 5, SRS §6). `docker-compose.db.yml` here is intentionally
  scoped to the database only and will be composed into that larger file
  on Day 5, not replaced by it.
- `.github/workflows/ci.yml` CI stub (Day 6, SRS §6)
