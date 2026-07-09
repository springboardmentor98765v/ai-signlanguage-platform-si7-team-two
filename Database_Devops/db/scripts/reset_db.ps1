# Postgres's docker-entrypoint-initdb.d scripts only run ONCE, the very
# first time a container starts against an empty data volume. If the
# reviewed schema changes (e.g. during Day 1/2 team review feedback),
# use this to wipe the volume and re-apply schema.sql + seed.sql cleanly.
# Usage: .\db\scripts\reset_db.ps1   (run from repo root)

Write-Host "This will DELETE all data in the signlang_postgres database and re-create it from scratch."
$confirm = Read-Host "Continue? [y/N]"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Aborted."
    exit 0
}

docker compose --env-file .env -f infra/docker-compose.db.yml down -v
docker compose --env-file .env -f infra/docker-compose.db.yml up -d

Write-Host "Waiting for Postgres to re-initialize..."
Start-Sleep -Seconds 5
& .\db\scripts\verify_connection.ps1
