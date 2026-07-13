#!/usr/bin/env bash
# Day 7 (SRS §6, Intern 5, Day 7): "run the full integration test."
#
# Scope honesty: the SRS's real Day 7 activity is the WHOLE TEAM walking
# through the actual learner journey (register -> login -> lesson ->
# practice -> real AI prediction -> real assessment -> real feedback ->
# real analytics) using Intern 1-4's real code (SRS §8.1). That can't be
# automated solo because that code doesn't exist in this engagement. This
# script is the closest solo equivalent: it exercises everything that IS
# real end-to-end — the full stack's containers, the backend's actual DB
# connectivity, the placeholder AI service's response contract, and the
# complete data-layer chain (practice session -> assessment -> feedback ->
# analytics) via the ORM. It does NOT prove Intern 1-4's real features
# work — only that the foundation they'll build on does.
#
# Prerequisite: the full stack must already be running
# (./db/scripts/start_full_stack.sh).
#
# Usage: ./db/scripts/integration_check.sh   (run from repo root)
set -uo pipefail

PASS=0
FAIL=0

check() {
  local description="$1"
  shift
  echo -n "[CHECK] $description ... "
  if "$@" >/tmp/integration_check_output.log 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
  else
    echo "FAIL"
    echo "  --- output ---"
    sed 's/^/  /' /tmp/integration_check_output.log
    FAIL=$((FAIL + 1))
  fi
}

echo "== Container-level health checks =="
check "backend /health responds"      curl -sf http://localhost:8000/health
check "backend /health/db responds"   curl -sf http://localhost:8000/health/db
check "ai-service /health responds"   curl -sf http://localhost:8001/health

echo ""
echo "== AI service response contract (placeholder) =="
check "ai-service /predict returns predicted_sign + confidence" bash -c \
  "curl -sf -X POST http://localhost:8001/predict | python3 -c \"
import json, sys
data = json.load(sys.stdin)
assert 'predicted_sign' in data, 'missing predicted_sign'
assert 'confidence' in data, 'missing confidence'
print(data)
\""

echo ""
echo "== Data layer: full ORM chain against the live database =="
check "verify_orm_models (structural check, all 8 tables)" python3 -m db.scripts.verify_orm_models
check "smoke_test_orm (roles/users/courses/lessons round trip)" python3 -m db.scripts.smoke_test_orm
check "smoke_test_full_journey (practice -> assessment -> feedback -> analytics)" python3 -m db.scripts.smoke_test_full_journey

echo ""
echo "============================================================"
echo "RESULT: $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then
  echo "All automatable checks passed. Real end-to-end verification with"
  echo "Intern 1-4's actual code (per SRS §8.1) is still a team activity,"
  echo "not something this script can do solo."
  exit 0
else
  echo "Some checks failed — see output above before considering the"
  echo "environment integrated."
  exit 1
fi
