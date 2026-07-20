"""
Database_Devops/backup/scripts/backup_db.py

Milestone 2, Day 6 — on-demand database backup script.
Reads DATABASE_URL (same env var used since Day 2) and writes a
timestamped file into ../backups/ (i.e. Database_Devops/backup/backups/).

Supports:
  - sqlite:///./dev.db                       → copies the .db file
  - postgresql+psycopg2://user:pass@host/db  → runs `pg_dump` (needs
                                               postgresql-client installed;
                                               free: apt-get / brew)

Usage:
    python Database_Devops/backup/scripts/backup_db.py

Optional: run daily via GitHub Actions — see
    .github/workflows/daily-backup.yml
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BACKUP_DIR = Path(__file__).resolve().parent.parent / "backups"


def backup_sqlite(database_url: str) -> Path:
    # sqlite:///./dev.db  →  ./dev.db
    db_path = Path(database_url.replace("sqlite:///", "", 1))
    if not db_path.exists():
        print(f"FAILED: SQLite file not found at {db_path}")
        sys.exit(1)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = BACKUP_DIR / f"backup_{timestamp}.db"
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.copy2(db_path, out_path)
    return out_path


def backup_postgres(database_url: str) -> Path:
    parsed = urlparse(database_url.replace("postgresql+psycopg2", "postgresql", 1))
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = BACKUP_DIR / f"backup_{timestamp}.sql"
    BACKUP_DIR.mkdir(exist_ok=True)

    env = os.environ.copy()
    if parsed.password:
        env["PGPASSWORD"] = parsed.password

    cmd = [
        "pg_dump",
        "-h", parsed.hostname or "localhost",
        "-p", str(parsed.port or 5432),
        "-U", parsed.username or "postgres",
        "-d", (parsed.path or "/postgres").lstrip("/"),
        "-f", str(out_path),
    ]

    try:
        subprocess.run(cmd, env=env, check=True)
    except FileNotFoundError:
        print(
            "FAILED: `pg_dump` is not installed.\n"
            "Install it (free): `apt-get install postgresql-client` "
            "or `brew install postgresql`."
        )
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"FAILED: pg_dump exited with an error: {exc}")
        sys.exit(1)

    return out_path


def main() -> None:
    database_url = os.environ.get("DATABASE_URL", "sqlite:///./dev.db")

    if database_url.startswith("sqlite"):
        out_path = backup_sqlite(database_url)
    elif database_url.startswith("postgresql"):
        out_path = backup_postgres(database_url)
    else:
        print(f"FAILED: unsupported DATABASE_URL scheme: {database_url}")
        sys.exit(1)

    size_kb = out_path.stat().st_size / 1024
    print(f"OK: backup written to {out_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
