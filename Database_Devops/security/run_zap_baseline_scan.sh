#!/usr/bin/env bash
# Milestone 3 - Day 7
# Basic free security scan against the LOCAL running app using OWASP ZAP's
# baseline scan (free, open-source, no live/public server touched).
#
# Usage:
#   docker compose -f docker-compose.test.yml up -d
#   ./security/run_zap_baseline_scan.sh http://localhost:8001

set -euo pipefail

TARGET_URL="${1:?Usage: ./run_zap_baseline_scan.sh <target_url>}"
REPORT_DIR="${REPORT_DIR:-./zap-reports}"
mkdir -p "$REPORT_DIR"

echo "Running OWASP ZAP baseline scan against $TARGET_URL ..."

docker run --rm \
    --network host \
    -v "$(pwd)/$REPORT_DIR:/zap/wrk:rw" \
    ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
    -t "$TARGET_URL" \
    -r zap_baseline_report.html \
    -J zap_baseline_report.json \
    || true  # zap-baseline.py exits non-zero if it finds warnings; don't fail the script on that

echo "Report written to $REPORT_DIR/zap_baseline_report.html"
echo "Review the report and list anything marked FAIL (not just WARN) in Day7_Summary.md"
