#!/usr/bin/env bash
# Milestone 3 - Day 5
# Re-tests the Milestone 2 backup process against the bigger Milestone 3
# database (now including badges, streaks, notifications).
#
# Usage:
#   DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db ./backup_db.sh

set -euo pipefail

DATABASE_URL="${DATABASE_URL:?Set DATABASE_URL first}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_FILE="${BACKUP_DIR}/sign_language_db_m3_${TIMESTAMP}.dump"

mkdir -p "$BACKUP_DIR"

echo "Backing up to $BACKUP_FILE ..."
pg_dump "$DATABASE_URL" --format=custom --file="$BACKUP_FILE"

echo "Verifying the backup includes the new Milestone 3 tables..."
pg_restore --list "$BACKUP_FILE" | grep -E "badges|streaks|notifications" \
    && echo "✅ badges, streaks, notifications all present in the backup" \
    || { echo "❌ one or more Milestone 3 tables missing from the backup!"; exit 1; }

echo "Backup complete: $BACKUP_FILE"
