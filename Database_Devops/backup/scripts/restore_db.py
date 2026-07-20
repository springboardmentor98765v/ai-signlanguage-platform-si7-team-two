"""
Database_Devops/backup/scripts/restore_db.py

Milestone 2, Day 6 — restore a backup produced by backup_db.py.
Works with both SQLite (.db file copy) and Postgres (.sql dump via psql).

Run:
    python Database_Devops/backup/scripts/restore_db.py \\
        Database_Devops/backup/backups/backup_20260722_140501.sql
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def restore_sqlite(database_url: str, backup_file: Path) -> None:
    db_path = Path(database_url.replace("sqlite:///", "", 1))
    shutil.copy2(backup_file, db_path)
    print(f"OK: {db_path} restored from {backup_file}")


def restore_postgres(database_url: str, backup_file: Path) -> None:
    parsed = urlparse(database_url.replace("postgresql+psycopg2", "postgresql", 1))

    env = os.environ.copy()
    if parsed.password:
        env["PGPASSWORD"] = parsed.password

    cmd = [
        "psql",
        "-h", parsed.hostname or "localhost",
        "-p", str(parsed.port or 5432),
        "-U", parsed.username or "postgres",
        "-d", (parsed.path or "/postgres").lstrip("/"),
        "-f", str(backup_file),
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
    except FileNotFoundError:
        print(
            "FAILED: `psql` is not installed.\n"
            "Install it (free): `apt-get install postgresql-client` "
            "or `brew install postgresql`."
        )
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"FAILED: psql exited with an error: {exc}")
        sys.exit(1)

    print(f"OK: database restored from {backup_file}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python Database_Devops/backup/scripts/restore_db.py <path-to-backup-file>")
        sys.exit(1)

    backup_file = Path(sys.argv[1])
    if not backup_file.exists():
        print(f"FAILED: backup file not found: {backup_file}")
        sys.exit(1)

    database_url = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

    print(f"About to restore INTO: {database_url.split('@')[-1]}")
    confirm = input("This will overwrite existing data. Type 'yes' to continue: ")
    if confirm.strip().lower() != "yes":
        print("Cancelled — nothing was restored.")
        sys.exit(0)

    if database_url.startswith("sqlite"):
        restore_sqlite(database_url, backup_file)
    elif database_url.startswith("postgresql"):
        restore_postgres(database_url, backup_file)
    else:
        print(f"FAILED: unsupported DATABASE_URL scheme: {database_url}")
        sys.exit(1)


if __name__ == "__main__":
    main()
