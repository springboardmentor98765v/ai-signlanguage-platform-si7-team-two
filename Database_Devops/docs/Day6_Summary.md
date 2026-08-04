# Milestone 3 — Day 6 (Intern 5: Database & QA Engineer)

## What was built

Local Docker Compose integration test setup — **no live/public deployment**,
per the Milestone 3 rule (deployment is reserved for Milestone 4). Everything
here runs against `docker-compose.test.yml` on localhost.

1. `docker-compose.test.yml` — spins up db + backend + AI service + frontend
   together, on non-conflicting local ports, using a dedicated
   `sign_language_db_test` database so it never touches dev/shared data.
2. `tests/test_learner_journey.py` — full learner flow: register → login →
   practice attempt → streak created/updated → notification generated →
   notification fetch returns it.
3. `tests/test_instructor_admin_journey.py` — instructor views the streak
   leaderboard; admin performs a bulk deactivate/reactivate.

## Also fixed (see `BUGFIX_NOTES.md` in docs)

Two integration-blocking bugs surfaced by teammates while testing against
this same stack:
- Alembic migration failure (`invalid input syntax for type uuid:
  "gen_random_uuid()"`) — fixed by wrapping the server default in
  `sa.text(...)` in both the migration and the ORM models.
- Mapper configuration failure (`Mapper 'Mapper[User(users)]' has no
  property 'streak'`) — fixed by adding the missing `streak`/`badges`
  relationships to `users.py` to match `Streak`/`Badge`'s `back_populates`.

Both are exactly the kind of thing this Day 6 test suite is meant to catch
locally before they reach someone else's branch — `test_learner_journey.py`
would have failed immediately on a fresh `alembic upgrade head` + mapper
configuration, instead of surfacing later in someone's Notification API work.

## How to run

```bash
docker compose -f docker-compose.test.yml up -d --build
# apply migrations against the test DB first:
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/sign_language_db_test alembic upgrade head

BASE_URL=http://localhost:8001 python tests/test_learner_journey.py
BASE_URL=http://localhost:8001 python tests/test_instructor_admin_journey.py

docker compose -f docker-compose.test.yml down -v
```

## Checkpoints

- [x] Docker Compose confirmed to start the entire local stack correctly
- [x] At least 2 full-journey local test scripts written
- [x] Tests run successfully against the local stack (after applying the Bug 1/Bug 2 fixes)
