# How to Run / Deploy This Project

A from-scratch guide for anyone who wasn't involved in building it —
covers both running everything locally and using the live, free-hosted
deployment.

## Option 1: Run it locally (fastest way to try it out)
Prerequisites: Docker Desktop (free) installed.

```bash
git clone <the repo>
cd <the repo>
cp .env.example .env
docker-compose up --build
```
That's it — one command brings up the database, backend, and AI service
together (see Day 7's `docker-compose.yml`). Frontend runs separately:
```bash
cd frontend
npm install
npm start
```

## Option 2: Use the already-deployed live version
No setup needed — just open the live links:
- **Frontend:** `<paste the real Netlify/Vercel URL here>`
- **Backend API docs (Swagger):** `<backend URL>/docs`

Note: free-tier hosting sleeps after inactivity. If it feels slow on the
very first request, that's normal — it's waking up, not broken.

## Project pieces and where they run
| Piece | Local (Docker) | Live (free hosting) |
|---|---|---|
| Frontend | `npm start` (port 3000) | Netlify / Vercel |
| Backend API | `docker-compose` (port 8000) | Render / Railway / Fly.io |
| AI service | `docker-compose` (port 8500) | Same host as backend, or separate |
| Database | `docker-compose` (local Postgres) | Free cloud Postgres (Supabase/Neon/ElephantSQL) |

## Checking everything is healthy
```bash
python day9/scripts/verify_full_stack.py \
    --frontend <frontend URL> \
    --backend <backend URL>
```

## Running the full learner-journey smoke test
```bash
python day10/scripts/smoke_test_full_journey.py --base-url <backend URL>
```
Walks through register → login → browse lessons → practice → score →
analytics, and reports pass/fail for each step.

## Backing up / restoring the database
See `day6/README_DAY6.md` — short version:
```bash
python day6/scripts/backup_db.py
python day6/scripts/restore_db.py <backup file>
```

## If something's down
1. Check the UptimeRobot dashboard (Day 8) first — it'll usually already
   have flagged which service is down.
2. Check the host's own dashboard (Render/Railway/Fly.io) for crash logs.
3. Confirm `DATABASE_URL` and other secrets are still set correctly in the
   host's environment variables — free tiers occasionally reset config on
   redeploy.
4. Worst case: bring it up locally with `docker-compose up --build` to
   confirm the code itself works, isolating whether the problem is the
   code or the hosting.

## Who owns what (for questions)
- Frontend / UI — Intern 1
- Backend & APIs (Auth, Lessons, Instructor/Admin) — Intern 2
- AI / Computer Vision (sign recognition model) — Intern 3
- Practice / Assessment / Feedback / Analytics / Certificates — Intern 4
- Database, Docker, hosting, backups, monitoring — Intern 5
