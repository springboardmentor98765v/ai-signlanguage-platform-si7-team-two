#!/usr/bin/env bash
# Postgres's docker-entrypoint-initdb.d scripts only run ONCE, the very
# first time a container starts against an empty data volume. If the
# reviewed schema changes (e.g. during Day 1/2 team review feedback),
# use this to wipe the volume and re-apply schema.sql + seed.sql cleanly.
# Usage: ./db/scripts/reset_db.sh   (run from repo root)
set -euo pipefail

echo "This will DELETE all data in the signlang_postgres database and re-create it from scratch."
read -p "Continue? [y/N] " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
  echo "Aborted."
  exit 0
fi

docker compose --env-file .env -f infra/docker-compose.db.yml down -v
docker compose --env-file .env -f infra/docker-compose.db.yml up -d

echo "Waiting for Postgres to re-initialize..."
sleep 5
./db/scripts/verify_connection.sh
