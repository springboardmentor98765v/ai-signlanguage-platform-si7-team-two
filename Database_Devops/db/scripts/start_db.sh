#!/usr/bin/env bash
# Day 2: bring up the shared Postgres instance and wait until it's healthy.
# Usage: ./db/scripts/start_db.sh   (run from repo root)
set -euo pipefail

if [ ! -f .env ]; then
  echo "ERROR: .env not found at repo root. Copy .env.example to .env first" \
       "(or ask Intern 5 for the shared dev .env)."
  exit 1
fi

docker compose --env-file .env -f infra/docker-compose.db.yml up -d

echo "Waiting for Postgres to become healthy..."
for i in $(seq 1 30); do
  status=$(docker inspect --format='{{.State.Health.Status}}' signlang_postgres 2>/dev/null || echo "starting")
  if [ "$status" = "healthy" ]; then
    echo "Postgres is healthy and ready on the port set in .env (DB_PORT)."
    exit 0
  fi
  sleep 1
done

echo "ERROR: Postgres did not become healthy within 30s. Run 'docker logs signlang_postgres' to inspect."
exit 1
