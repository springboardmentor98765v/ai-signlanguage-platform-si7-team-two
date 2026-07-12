# Day 7 (SRS §6, Intern 5, Day 7): "run the full integration test."
# See the header comment in integration_check.sh for the full scope-honesty
# note — this is the closest solo equivalent to the SRS's team activity.
#
# Prerequisite: the full stack must already be running
# (.\db\scripts\start_full_stack.ps1).
#
# Usage: .\db\scripts\integration_check.ps1   (run from repo root)

$pass = 0
$fail = 0

function Check($description, $scriptBlock) {
    Write-Host -NoNewline "[CHECK] $description ... "
    try {
        & $scriptBlock | Out-Null
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) { throw "non-zero exit" }
        Write-Host "PASS"
        $script:pass++
    } catch {
        Write-Host "FAIL"
        Write-Host "  $_"
        $script:fail++
    }
}

Write-Host "== Container-level health checks =="
Check "backend /health responds" { curl.exe -sf http://localhost:8000/health }
Check "backend /health/db responds" { curl.exe -sf http://localhost:8000/health/db }
Check "ai-service /health responds" { curl.exe -sf http://localhost:8001/health }

Write-Host ""
Write-Host "== Data layer: full ORM chain against the live database =="
Check "verify_orm_models (structural check, all 8 tables)" { python -m db.scripts.verify_orm_models }
Check "smoke_test_orm (roles/users/courses/lessons round trip)" { python -m db.scripts.smoke_test_orm }
Check "smoke_test_full_journey (practice -> assessment -> feedback -> analytics)" { python -m db.scripts.smoke_test_full_journey }

Write-Host ""
Write-Host "============================================================"
Write-Host "RESULT: $pass passed, $fail failed"
if ($fail -eq 0) {
    Write-Host "All automatable checks passed. Real end-to-end verification with"
    Write-Host "Intern 1-4's actual code (per SRS section 8.1) is still a team activity,"
    Write-Host "not something this script can do solo."
    exit 0
} else {
    Write-Host "Some checks failed - see output above before considering the"
    Write-Host "environment integrated."
    exit 1
}
