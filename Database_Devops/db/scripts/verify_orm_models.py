"""
db/scripts/verify_orm_models.py

Day 3 verification (SRS §6, Intern 5, Day 3: "verify with Intern 2's
User/Course Service"). Honest scope note: Intern 2's actual FastAPI service
isn't part of this solo engagement, so this script does the closest
available solo equivalent — it connects to the real, running Day 2
database and checks that every column the ORM models declare actually
exists on the live table, with a matching nullability. When Intern 2's
service is available, that remains the real integration check to run.

Usage (run from repo root):
    python -m db.scripts.verify_orm_models
"""
import sys

from sqlalchemy import inspect

from db.database import engine
from db.models import Base

# Only the 4 tables in Day 3's scope.
DAY3_TABLES = ["roles", "users", "courses", "lessons"]


def verify() -> bool:
    inspector = inspect(engine)
    live_tables = set(inspector.get_table_names())
    all_ok = True

    for table_name in DAY3_TABLES:
        print(f"\n== {table_name} ==")
        if table_name not in live_tables:
            print(f"  FAIL: table '{table_name}' does not exist in the live database.")
            all_ok = False
            continue

        live_columns = {c["name"]: c for c in inspector.get_columns(table_name)}
        model_columns = Base.metadata.tables[table_name].columns

        for col in model_columns:
            live_col = live_columns.get(col.name)
            if live_col is None:
                print(f"  FAIL: column '{col.name}' declared in ORM model but missing in DB.")
                all_ok = False
                continue

            model_nullable = col.nullable
            live_nullable = live_col["nullable"]
            if model_nullable != live_nullable:
                print(
                    f"  FAIL: column '{col.name}' nullable mismatch "
                    f"(model={model_nullable}, db={live_nullable})"
                )
                all_ok = False
                continue

            print(f"  OK: {col.name}")

        extra_in_db = set(live_columns) - {c.name for c in model_columns}
        if extra_in_db:
            print(f"  NOTE: DB has columns not in the ORM model: {sorted(extra_in_db)}")

    return all_ok


if __name__ == "__main__":
    print("Verifying Day 3 ORM models (roles, users, courses, lessons) against the live database...")
    ok = verify()
    print("\n" + ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED — see FAIL lines above"))
    sys.exit(0 if ok else 1)
