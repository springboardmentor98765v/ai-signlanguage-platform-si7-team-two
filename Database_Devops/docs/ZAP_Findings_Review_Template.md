# OWASP ZAP Baseline Scan — Findings Review (Day 7)

Fill this in after running `run_zap_baseline_scan.sh` against the local
Docker Compose stack (`docker-compose.test.yml` from Day 6).

## How to review
1. Open `zap-reports/zap_baseline_report.html` in a browser.
2. For every alert, note its **Risk level** (High / Medium / Low / Informational).
3. Anything **High** or **Medium** goes in the table below and gets flagged
   to Intern 2 (backend) the same day — don't wait until Day 8.
4. **Low**/**Informational** items are logged here too, but can wait.

## Findings

| Risk | Alert | Affected endpoint(s) | Owner to fix | Status |
|---|---|---|---|---|
| _fill in from your actual scan output_ | | | | |

## Common findings to specifically check for (from the ZAP baseline ruleset)
- Missing security headers (`X-Content-Type-Options`, `X-Frame-Options`,
  `Content-Security-Policy`)
- CORS misconfiguration (wildcard `*` origin on authenticated endpoints)
- Cookies without `Secure`/`HttpOnly`/`SameSite` flags
- Verbose error messages leaking stack traces or internal paths
- Missing rate limiting on auth endpoints (cross-check against Intern 2's
  Day 6 per-user rate limiting work)

## Sign-off

- [ ] Scan run and report saved to `zap-reports/`
- [ ] All High/Medium findings listed above and assigned an owner
- [ ] No critical (High-risk) issues left unaddressed by end of Day 8
