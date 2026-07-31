#!/usr/bin/env bash
# Milestone 3 - Day 5
# Restores a backup into a scratch database and confirms row counts match
# the source, for every table including the new Milestone 3 ones.
#
# Usage:
#   SOURCE_DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db \
#   RESTORE_DATABASE_URL=postgresql://user:pass@host:5432/sign_language_db_restore_test \
#   ./restore_db.sh ./backups/sign_language_db_m3_20260731_...dump

set -euo pipefail

BACKUP_FILE="${1:?Usage: ./restore_db.sh <backup_file>}"
SOURCE_DATABASE_URL="${SOURCE_DATABASE_URL:?Set SOURCE_DATABASE_URL}"
RESTORE_DATABASE_URL="${RESTORE_DATABASE_URL:?Set RESTORE_DATABASE_URL (a scratch/test DB, not production)}"

RESTORE_DB_NAME=$(basename "$RESTORE_DATABASE_URL")

echo "Creating scratch database ${RESTORE_DB_NAME} for the restore test..."
createdb "$RESTORE_DB_NAME" 2>/dev/null || echo "(scratch DB already exists, reusing it)"

echo "Restoring $BACKUP_FILE into $RESTORE_DATABASE_URL ..."
pg_restore --clean --if-exists --no-owner --dbname="$RESTORE_DATABASE_URL" "$BACKUP_FILE"

echo ""
echo "Comparing row counts (source vs restored)..."
TABLES=(users lessons practice_sessions assessments feedback certificates \
         recommendations instructor_student badges streaks notifications)

FAILED=0
for table in "${TABLES[@]}"; do
    src_count=$(psql "$SOURCE_DATABASE_URL" -tAc "SELECT COUNT(*) FROM $table" 2>/dev/null || echo "N/A")
    dst_count=$(psql "$RESTORE_DATABASE_URL" -tAc "SELECT COUNT(*) FROM $table" 2>/dev/null || echo "N/A")

    if [[ "$src_count" == "$dst_count" ]]; then
        echo "✅ $table: $src_count rows match"
    else
        echo "❌ $table: source=$src_count restored=$dst_count — MISMATCH"
        FAILED=1
    fi
done

if [[ "$FAILED" -eq 0 ]]; then
    echo ""
    echo "✅ Restore verified successfully — all tables (including badges, streaks, notifications) match."
else
    echo ""
    echo "❌ Restore verification failed — see mismatches above."
    exit 1
fi
