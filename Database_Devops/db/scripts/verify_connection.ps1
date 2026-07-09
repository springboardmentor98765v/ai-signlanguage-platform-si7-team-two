# Day 2 verification: confirm the running Postgres instance has all 8
# tables from the reviewed ERD, and that seed data loaded correctly.
# Runs psql INSIDE the container, so no local psql client is required.
# Usage: .\db\scripts\verify_connection.ps1   (run from repo root)

Write-Host "== Tables present =="
docker exec -i signlang_postgres psql -U signlang_app -d signlang_platform -c "\dt"

Write-Host ""
Write-Host "== Expected: 8 tables (roles, users, courses, lessons, practice_sessions, assessments, feedback, learner_analytics) =="

Write-Host ""
Write-Host "== Seed check: roles =="
docker exec -i signlang_postgres psql -U signlang_app -d signlang_platform -c "SELECT name FROM roles ORDER BY name;"

Write-Host ""
Write-Host "== Seed check: seeded lessons =="
docker exec -i signlang_postgres psql -U signlang_app -d signlang_platform -c "SELECT letter, title FROM lessons ORDER BY order_index;"

Write-Host ""
Write-Host "If you see 4 roles and 5 lessons (A, B, C, L, Y) above, Day 2 setup is verified."
