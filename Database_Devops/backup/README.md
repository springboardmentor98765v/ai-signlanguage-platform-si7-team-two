# Database_Devops/backup — Milestone 2, Day 6 (Intern 5)

## What this is
An on-demand (and optionally daily) backup/restore system for the project
database. Supports both SQLite (local dev) and PostgreSQL (the free cloud DB
from Day 4).

## Folder structure
```
backup/
├── scripts/
│   ├── backup_db.py    # makes a timestamped backup
│   └── restore_db.py   # restores from a backup file (asks for confirmation)
├── backups/             # backup files land here (.gitkeep keeps it in git)
└── README.md           (this file)
```

## How to make a backup (on demand)
```bash
# From the repo root:
pip install python-dotenv
python Database_Devops/backup/scripts/backup_db.py
```
Reads `DATABASE_URL` from `.env` and:
- If SQLite → copies the `.db` file into `backup/backups/`
- If PostgreSQL → runs `pg_dump` and saves a `.sql` file into `backup/backups/`

Each file is timestamped (`backup_20260722_140501.sql`) so nothing gets overwritten.

## How to restore from a backup
```bash
python Database_Devops/backup/scripts/restore_db.py \
    Database_Devops/backup/backups/backup_20260722_140501.sql
```
The script shows you which database it's about to restore into and asks
you to type **`yes`** to confirm — this exists on purpose, because restoring
overwrites whatever data is currently there.

> ⚠️ **Only type `yes` once you are sure.** Anything other than `yes` cancels
> safely with no changes made.

## Optional: automatic daily backups via GitHub Actions (free)
`.github/workflows/daily-backup.yml` runs `backup_db.py` every day at
02:00 UTC and uploads the result as a downloadable workflow artifact —
completely free on GitHub's free tier.

To activate it:
1. In GitHub: **Settings → Secrets and variables → Actions → New repository
   secret** → name it `DATABASE_URL`, paste the real connection string.
2. Push. Check the **Actions** tab the next day, or trigger it manually via
   "Run workflow" to confirm it worked.

## Notes
- PostgreSQL backups require `pg_dump` / `psql` installed locally. Install free:
  - `sudo apt-get install postgresql-client` (Ubuntu/Debian / GitHub Actions)
  - `brew install postgresql` (macOS)
- `backups/` is gitignored for backup *files*; `backups/.gitkeep` keeps the
  folder itself in version control. Actual backup files should not be committed.
