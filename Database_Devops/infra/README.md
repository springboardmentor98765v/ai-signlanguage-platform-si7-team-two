# Infrastructure (Intern 5)

Empty on Day 1 by design. This folder will hold:
- `Dockerfile.backend`, `Dockerfile.ai-service` (Day 5, SRS §6)
- `docker-compose.yml` (Day 5, SRS §6)
- `.github/workflows/ci.yml` CI stub (Day 6, SRS §6)

Building these now would be premature: the schema in `db/` is still pending
team review, and standing up containers before the ERD is approved risks
exactly the rework scenario flagged in SRS §9 ("Database schema changes
mid-week breaking backend code").
