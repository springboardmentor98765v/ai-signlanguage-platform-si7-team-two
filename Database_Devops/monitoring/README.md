# Database_Devops/monitoring — Milestone 2, Day 8 (Intern 5)

## What this is
Free uptime monitoring (UptimeRobot) + a local companion check script +
a simple Apache Bench load test — no paid tools required anywhere.

## Folder structure
```
monitoring/
├── scripts/
│   ├── check_uptime.py    # quick manual uptime check; logs to results/
│   └── load_test.sh       # wraps Apache Bench; saves output to results/
├── results/                # test output lands here (.gitkeep keeps it in git)
└── README.md              (this file)
```

## Part 1 — UptimeRobot (primary, ~5 minute setup)
1. Create a free account at [uptimerobot.com](https://uptimerobot.com).
   Free tier: up to 50 monitors, pings every 5 minutes.
2. **Add New Monitor**:
   - Type: `HTTP(s)`
   - Friendly Name: `Sign Language Backend`
   - URL: live backend URL from Day 5 + `/health`
     (e.g. `https://sign-language-backend.onrender.com/health`)
   - Interval: 5 minutes
3. Save. UptimeRobot emails the team automatically if the backend goes down.
4. Optional: create a free public status page (UptimeRobot → Status Pages)
   so the whole team can see uptime without logging in.

## Part 2 — local companion check (no signup needed)
```bash
python Database_Devops/monitoring/scripts/check_uptime.py \
    https://sign-language-backend.onrender.com/health
```
Logs a line to `results/uptime_log.csv` each time it's run (`UP`/`DOWN`,
HTTP status, response time in ms). Useful for a quick sanity check before
a demo.

## Part 3 — load test with Apache Bench
```bash
bash Database_Devops/monitoring/scripts/load_test.sh \
    https://sign-language-backend.onrender.com/health \
    50 5
```
Arguments: URL, total requests (default 50), concurrency (default 5).

If `ab` is not installed:
- Ubuntu/Debian: `sudo apt-get install apache2-utils`
- macOS: usually preinstalled; otherwise `brew install httpd`

Full output is saved to `results/load_test_<timestamp>.txt`.

### What to look for
| Metric | What matters |
|--------|-------------|
| Requests/sec | Free-tier hosts are modest; expect low numbers |
| Failed requests | Should be 0 |
| Mean time/request | Run twice; use the second run (avoids cold-start bias) |

### Reporting results to the team (paste into stand-up chat)
```
Load test — <date>
URL: <backend URL>
Requests: 50, Concurrency: 5
Requests/sec: <value>
Failed requests: <value>
Mean time/request: <value> ms
Notes: <e.g. "first request slow due to free-tier cold start, fine otherwise">
```

## Notes
- Both UptimeRobot and Apache Bench are entirely free — no paid tools required.
- Keep load test request counts modest (50–100); free hosting can rate-limit
  traffic that looks like an attack at higher counts.
