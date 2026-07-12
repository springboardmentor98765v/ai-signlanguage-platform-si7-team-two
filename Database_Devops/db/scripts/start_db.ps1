# Day 2: bring up the shared Postgres instance and wait until it's healthy.
# Usage: .\db\scripts\start_db.ps1   (run from repo root)

if (-not (Test-Path ".env")) {
    Write-Error "ERROR: .env not found at repo root. Copy .env.example to .env first (or ask Intern 5 for the shared dev .env)."
    exit 1
}

docker compose --env-file .env -f infra/docker-compose.db.yml up -d

Write-Host "Waiting for Postgres to become healthy..."
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    $status = docker inspect --format='{{.State.Health.Status}}' signlang_postgres 2>$null
    if ($status -eq "healthy") {
        $ready = $true
        break
    }
    Start-Sleep -Seconds 1
}

if ($ready) {
    Write-Host "Postgres is healthy and ready on the port set in .env (DB_PORT)."
} else {
    Write-Error "ERROR: Postgres did not become healthy within 30s. Run 'docker logs signlang_postgres' to inspect."
    exit 1
}
