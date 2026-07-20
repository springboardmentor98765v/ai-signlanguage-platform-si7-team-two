"""
Database_Devops/monitoring/scripts/check_uptime.py

Milestone 2, Day 8 — simple uptime check script.

UptimeRobot (free tier) is the primary monitor — see README_DAY8.md for
the 5-minute signup. This script is a small companion/fallback: run it
manually (or on a cron) to log whether the live backend responded, in
case anyone wants a quick check without opening the UptimeRobot dashboard.

Run:
    python Database_Devops/monitoring/scripts/check_uptime.py \\
        https://sign-language-backend.onrender.com/health
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

LOG_FILE = Path(__file__).resolve().parent.parent / "results" / "uptime_log.csv"


def check(url: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    start = time.time()
    try:
        with urlopen(url, timeout=10) as response:
            elapsed_ms = round((time.time() - start) * 1000)
            status = response.status
            result = "UP"
    except URLError as exc:
        elapsed_ms = round((time.time() - start) * 1000)
        status = "ERROR"
        result = "DOWN"
        print(f"[{timestamp}] DOWN — {exc}")
    else:
        print(f"[{timestamp}] UP — status {status}, {elapsed_ms}ms")

    LOG_FILE.parent.mkdir(exist_ok=True)
    is_new_file = not LOG_FILE.exists()
    with open(LOG_FILE, "a") as f:
        if is_new_file:
            f.write("timestamp,result,status,elapsed_ms\n")
        f.write(f"{timestamp},{result},{status},{elapsed_ms}\n")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python Database_Devops/monitoring/scripts/check_uptime.py <url>")
        sys.exit(1)
    check(sys.argv[1])


if __name__ == "__main__":
    main()
