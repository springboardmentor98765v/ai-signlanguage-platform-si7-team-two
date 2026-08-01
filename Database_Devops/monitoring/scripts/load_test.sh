#!/usr/bin/env bash
# Database_Devops/monitoring/scripts/load_test.sh
#
# Milestone 2, Day 8 — simple free load test using Apache Bench (`ab`).
#
# `ab` ships with apache2-utils (Linux) or the Apache HTTP Server on
# macOS/Windows — free, no signup needed.
#
# Usage (from repo root):
#   bash Database_Devops/monitoring/scripts/load_test.sh \
#        https://sign-language-backend.onrender.com/health
#   bash Database_Devops/monitoring/scripts/load_test.sh \
#        https://sign-language-backend.onrender.com/health 100 10
#
# Args:
#   $1 = URL to test              (required)
#   $2 = total number of requests (default: 50)
#   $3 = concurrency level        (default: 5)
#
# Keep request counts modest on free-tier hosts (50-100); higher counts can
# trigger rate-limiting.  Run twice and use the second run's numbers to
# avoid cold-start bias.

set -euo pipefail

URL="${1:?Usage: ./load_test.sh <url> [requests] [concurrency]}"
REQUESTS="${2:-50}"
CONCURRENCY="${3:-5}"

if ! command -v ab > /dev/null 2>&1; then
  echo "ERROR: 'ab' (Apache Bench) is not installed."
  echo "Install it (free):"
  echo "  Ubuntu/Debian: sudo apt-get install apache2-utils"
  echo "  macOS:         comes preinstalled, or 'brew install httpd'"
  exit 1
fi

echo "Load testing: $URL"
echo "Requests: $REQUESTS | Concurrency: $CONCURRENCY"
echo "----------------------------------------------------"

RESULTS_DIR="$(dirname "$0")/../results"
mkdir -p "$RESULTS_DIR"
TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
OUT_FILE="$RESULTS_DIR/load_test_${TIMESTAMP}.txt"

ab -n "$REQUESTS" -c "$CONCURRENCY" "$URL" | tee "$OUT_FILE"

echo "----------------------------------------------------"
echo "Full results saved to: $OUT_FILE"
