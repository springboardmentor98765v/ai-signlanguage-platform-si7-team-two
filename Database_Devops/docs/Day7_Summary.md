# Milestone 3 — Day 7 (Intern 5: Database & QA Engineer)

## What was built

Basic free security testing against the **local** running app (from Day 6's
Docker Compose stack) — no live/public server touched.

1. `security/run_zap_baseline_scan.sh` — runs OWASP ZAP's free baseline
   scan (via its official Docker image) against a target URL and saves an
   HTML + JSON report.
2. `docs/ZAP_Findings_Review_Template.md` — structured template for
   triaging the scan output: every High/Medium finding gets a named owner
   the same day, not left for later.

## How to run

```bash
# 1. Bring up the local test stack (from Day 6)
docker compose -f docker-compose.test.yml up -d

# 2. Run the scan against it
./security/run_zap_baseline_scan.sh http://localhost:8001

# 3. Open the report and fill in ZAP_Findings_Review_Template.md
open zap-reports/zap_baseline_report.html  # or just open it in a browser
```

## Checkpoints

- [x] Free security tool (OWASP ZAP) installed/runnable and executed against the local app
- [ ] Scan results reviewed — **fill in `ZAP_Findings_Review_Template.md` with your actual findings**
- [ ] Any serious (High/Medium) issues found are listed for fixing — assign an owner the same day
