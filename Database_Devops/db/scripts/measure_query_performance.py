"""
Milestone 3 - Day 3
Measures query speed BEFORE and AFTER adding each performance index,
using EXPLAIN ANALYZE so the numbers are real planner/execution times,
not just wall-clock noise from network latency.

Usage:
    DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname python measure_query_performance.py

Requires the tables to already have a reasonable amount of data — for a
meaningful before/after comparison on a laptop-sized dataset, this script
can optionally seed extra rows first (see SEED_ROWS below).
"""
import os
import re
import time

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/sign_language_db",
)
engine = create_engine(DATABASE_URL)

# Toggle to insert extra rows so the before/after difference is visible
# even on a small local dataset. Safe to run multiple times (uses ON CONFLICT).
SEED_ROWS = int(os.getenv("SEED_ROWS", "0"))

QUERIES = {
    "users_by_email": {
        "sql": "SELECT * FROM users WHERE email = 'sample_learner_999@example.com'",
        "index_name": "ix_users_email",
        "index_sql": "CREATE INDEX ix_users_email ON users (email)",
        "table": "users",
    },
    "lessons_by_category": {
        "sql": "SELECT * FROM lessons WHERE category = 'Alphabet'",
        "index_name": "ix_lessons_category",
        "index_sql": "CREATE INDEX ix_lessons_category ON lessons (category)",
        "table": "lessons",
    },
    "badges_by_learner": {
        "sql": (
            "SELECT * FROM badges "
            "WHERE learner_id = (SELECT id FROM users ORDER BY random() LIMIT 1)"
        ),
        "index_name": "ix_badges_learner_id",
        "index_sql": "CREATE INDEX ix_badges_learner_id ON badges (learner_id)",
        "table": "badges",
    },
}


def explain_analyze_time(conn, sql: str) -> float:
    """Runs EXPLAIN ANALYZE and returns the reported 'Execution Time' in ms."""
    result = conn.execute(text(f"EXPLAIN ANALYZE {sql}"))
    plan_lines = [row[0] for row in result]
    for line in plan_lines:
        match = re.search(r"Execution Time: ([\d.]+) ms", line)
        if match:
            return float(match.group(1))
    return -1.0  # couldn't parse; inspect plan_lines manually


def drop_index_if_exists(conn, index_name: str):
    conn.execute(text(f"DROP INDEX IF EXISTS {index_name}"))


def run_comparison():
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")

        for label, q in QUERIES.items():
            print(f"\n=== {label} ===")

            drop_index_if_exists(conn, q["index_name"])
            before_ms = explain_analyze_time(conn, q["sql"])
            print(f"BEFORE index:  {before_ms:.3f} ms")

            conn.execute(text(q["index_sql"]))
            after_ms = explain_analyze_time(conn, q["sql"])
            print(f"AFTER index:   {after_ms:.3f} ms")

            if before_ms > 0 and after_ms > 0:
                improvement = (before_ms - after_ms) / before_ms * 100
                print(f"Improvement:   {improvement:.1f}%")


if __name__ == "__main__":
    start = time.time()
    run_comparison()
    print(f"\nDone in {time.time() - start:.1f}s")
