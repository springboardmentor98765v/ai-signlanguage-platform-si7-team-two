#!/usr/bin/env bash
# Day 5: bring up the full stack (db + backend + ai-service) with one command.
# Usage: ./db/scripts/start_full_stack.sh   (run from repo root)
set -euo pipefail

if [ ! -f .env ]; then
  echo "ERROR: .env not found at repo root. Copy .env.example to .env first."
  exit 1
fi

# The full stack and the db-only compose file both manage a container
# named signlang_postgres — stop the db-only one first if it's running,
# to avoid a name/port conflict.
docker compose -f infra/docker-compose.db.yml down 2>/dev/null || true

docker compose --env-file .env -f infra/docker-compose.yml up -d --build

echo "Waiting for the database to become healthy..."
for i in $(seq 1 30); do
  status=$(docker inspect --format='{{.State.Health.Status}}' signlang_postgres 2>/dev/null || echo "starting")
  if [ "$status" = "healthy" ]; then
    break
  fi
  sleep 1
done

echo ""
echo "Stack is up. Check status with: docker compose -f infra/docker-compose.yml ps"
echo "  backend:    http://localhost:8000/health   and /health/db"
echo "  ai-service: http://localhost:8001/health"
