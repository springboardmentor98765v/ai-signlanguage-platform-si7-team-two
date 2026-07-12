# Day 5: bring up the full stack (db + backend + ai-service) with one command.
# Usage: .\db\scripts\start_full_stack.ps1   (run from repo root)

if (-not (Test-Path ".env")) {
    Write-Error "ERROR: .env not found at repo root. Copy .env.example to .env first."
    exit 1
}

# The full stack and the db-only compose file both manage a container
# named signlang_postgres — stop the db-only one first if it's running.
docker compose -f infra/docker-compose.db.yml down 2>$null

docker compose --env-file .env -f infra/docker-compose.yml up -d --build

Write-Host "Waiting for the database to become healthy..."
for ($i = 0; $i -lt 30; $i++) {
    $status = docker inspect --format='{{.State.Health.Status}}' signlang_postgres 2>$null
    if ($status -eq "healthy") { break }
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "Stack is up. Check status with: docker compose -f infra/docker-compose.yml ps"
Write-Host "  backend:    http://localhost:8000/health   and /health/db"
Write-Host "  ai-service: http://localhost:8001/health"
