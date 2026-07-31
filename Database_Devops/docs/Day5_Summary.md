# Milestone 3 — Day 5 (Intern 5: Database & QA Engineer)

## What was retested

The backup/restore process built in Milestone 2 (Day 6), re-run against the
now-larger Milestone 3 database — which includes `badges`, `streaks`, and
`notifications` on top of everything from M1/M2.

## Files

- `scripts/backup_db.sh` — takes a `pg_dump` backup and verifies the new M3
  tables are actually present inside the dump (not just an assumption)
- `scripts/restore_db.sh` — restores that backup into a scratch database and
  compares row counts, table by table, so a silent partial restore can't slip
  through unnoticed

## How to run

```bash
# 1. Take a backup
DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db \
    ./scripts/backup_db.sh

# 2. Restore it into a scratch DB and verify
SOURCE_DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db \
RESTORE_DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db_restore_test \
    ./scripts/restore_db.sh ./backups/sign_language_db_m3_<timestamp>.dump
```

## Plain-language restore steps (for anyone on the team, not just Intern 5)

1. Get the latest `.dump` file from the `backups/` folder (or wherever it's
   shared with the team).
2. Create a new, empty database to restore into — **never restore directly
   over the live database** without a second backup of that first.
3. Run `restore_db.sh <the dump file>` and check that every table prints a ✅.
4. If anything shows a ❌ mismatch, don't discard the backup — flag it in the
   team channel so Intern 5 can investigate before relying on that backup.

## Checkpoints

- [x] Backup taken of the current, larger (Milestone 3) database
- [x] Restore tested successfully from that backup, including badges/streaks/notifications
- [x] No issues found with backup/restore against the bigger schema
