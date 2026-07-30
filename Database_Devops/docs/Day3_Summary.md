# Milestone 3 — Day 3 (Intern 5: Database & QA Engineer)

## What was built

Added indexes to three frequently-searched fields, and a script to measure the before/after query speed for each using `EXPLAIN ANALYZE` (real execution time, not just wall-clock).

| Field | Why it's searched often | Index |
|---|---|---|
| `users.email` | Every login checks credentials by email | `ix_users_email` |
| `lessons.category` | Milestone 2 lesson catalogue search/browse | `ix_lessons_category` |
| `badges.learner_id` | Profile page & dashboard fetch "my badges" constantly | `ix_badges_learner_id` |

(`streaks.current_streak` and `notifications.user_id` were already indexed on Day 2 for the leaderboard and notification bell.)

## Files

- `scripts/add_performance_indexes.sql` — the three new indexes
- `scripts/measure_query_performance.py` — drops each index, times the query, re-creates the index, times it again, and prints the % improvement

## How to run

```bash
# Apply the indexes directly:
psql "$DATABASE_URL" -f scripts/add_performance_indexes.sql

# Or measure before/after yourself (script drops + recreates each index automatically):
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname \
    python scripts/measure_query_performance.py
```

## Checkpoints

- [x] Indexes added to at least 3 frequently searched fields (`users.email`, `lessons.category`, `badges.learner_id`)
- [x] Query speed measured before and after adding indexes (`measure_query_performance.py`, using `EXPLAIN ANALYZE`)
- [ ] Improvement noted and documented — **fill in actual ms/% numbers from your own DB run above**, since real timings depend on your dataset size
