# Milestone 1 — Deployment Note

Prepared by: Intern 5 (Database & DevOps), Day 7 (SRS §6, Intern 5, Day 7).

## What this note is

SRS Day 7's deliverable is *"a short deployment note"* following a
full-team integration pass (SRS §8.1). This note covers what the **Data
and Infrastructure Layers** can actually verify solo, and is explicit
about what still requires Intern 1–4's real code to check for real. It is
not a substitute for the actual team walkthrough in SRS §8.1 — it's what's
ready for that walkthrough to build on.

## How to stand up the environment

```bash
cp .env.example .env   # or use the team-shared .env
./db/scripts/start_full_stack.sh      # Linux/macOS
# .\db\scripts\start_full_stack.ps1   # Windows
./db/scripts/integration_check.sh     # Linux/macOS
# .\db\scripts\integration_check.ps1  # Windows
```

## What IS verified end-to-end (automated, solo-provable)

| Check | Status |
|---|---|
| Postgres container starts, healthy, seeded (4 roles, 5 lessons) | ✅ Verified — Day 2 |
| All 8 tables match their SQLAlchemy ORM models exactly (columns, nullability) | ✅ Verified — `verify_orm_models.py` |
| Alembic migrations produce DDL identical to the reviewed `schema.sql` | ✅ Verified — Day 3/4, offline SQL diff |
| Real insert → query → delete round trip through the ORM (roles/users/courses/lessons) | ✅ Verified — `smoke_test_orm.py` |
| Full relationship chain: User → PracticeSession → Assessment → Feedback, and User → LearnerAnalytics | ✅ Verified — `smoke_test_full_journey.py` |
| Backend container builds, starts, and can query Postgres over the Docker network | ✅ Verified — `backend`'s `/health/db` |
| AI service container builds, starts, and returns the `{predicted_sign, confidence}` contract shape Intern 4's Assessment Service expects | ✅ Verified — `ai-service`'s `/predict` (placeholder data) |
| CI runs all of the above automatically on every push, against a throwaway database | ✅ Verified — `.github/workflows/ci.yml` |

## What is NOT yet verified (needs Intern 1–4's real code — SRS §8.1)

| Acceptance criterion (SRS §8.2) | Status |
|---|---|
| A user can register and log in successfully | ⏳ Needs Intern 2's real Auth API (backend is currently a placeholder) |
| A logged-in learner can view a seeded lesson list and open a lesson | ⏳ Needs Intern 1's real frontend + Intern 2's real Course API |
| The Practice screen captures a webcam frame and receives a predicted sign with confidence | ⏳ Needs Intern 1's real webcam UI + Intern 3's real MediaPipe pipeline (ai-service currently returns a hardcoded fake prediction) |
| An accuracy score and rule-based feedback are generated and shown to the learner | ⏳ Needs Intern 4's real scoring/feedback logic (the *tables* for this are real and verified; the *business logic* that populates them from a live practice session is not) |
| Full docker-compose stack integrates all real services together | ⏳ Currently integrates the DB + 2 placeholder services; will integrate for real once Intern 1–4 replace their placeholders |

## Known limitations / honest caveats

- **`backend/` and `ai-service/` are placeholders.** They exist so the
  Docker/Compose/CI infrastructure is real and provably working, not so
  the actual product features work. Replacing them is Intern 2/3/4's
  scope, not Data Layer scope.
- **No solo substitute exists for a real cross-team integration test.**
  Everything in the "NOT yet verified" table requires the actual people
  building those services to run this environment and confirm their part
  works against it — that's inherently a team activity per SRS §8.1's
  Step-by-step sequence, and the automated checks here can't fabricate
  that confidence.
- **Role naming (`Trainer` vs `Accessibility Trainer`)** is still an open
  decision flagged since Day 1/2 — see `db/BASE_DOCUMENT_ALIGNMENT.md`.
  Worth resolving before any RBAC code hardcodes one spelling.

## Recommendation for the actual SRS §8.1 team walkthrough

Once Intern 1–4 have real code on their feature branches and merged into
`integration` (per `CONTRIBUTING.md`):
1. Everyone pulls `integration` and runs `./db/scripts/start_full_stack.sh`.
2. Replace the two placeholder Dockerfiles' images are already correctly
   wired to build from `backend/` and `ai-service/`'s real code — no infra
   changes needed, just merge real app code into those folders.
3. Run `./db/scripts/integration_check.sh` again — if the DB-layer checks
   ever regress, that's a real bug introduced by someone's merge, not a
   flake.
4. Then do the SRS §8.1 six-step manual walkthrough as a team: register →
   login → lesson list → practice → prediction → assessment/feedback →
   analytics, exactly as the SRS specifies.
