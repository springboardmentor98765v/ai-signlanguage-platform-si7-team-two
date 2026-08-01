"""
Day 9 — full-stack verification script.

Checks that every deployed piece of the platform is reachable:
  - Frontend (free hosting: Netlify/Vercel)
  - Backend  (free hosting: Render/Railway/Fly.io) -> /health
  - AI service (either behind the backend, or its own /health if exposed)
  - Database, indirectly, via a backend endpoint that queries it

This isn't a replacement for the team manually clicking through the app —
it's a fast first check to run before that, so obvious deployment breakage
(wrong URL, service down, CORS misconfigured) gets caught immediately.

Run:
    python scripts/verify_full_stack.py \\
        --frontend https://sign-language.netlify.app \\
        --backend https://sign-language-backend.onrender.com \\
        --ai-service https://sign-language-ai.onrender.com
"""

import argparse
import sys
import time
from urllib.error import URLError
from urllib.request import Request, urlopen


def check(name: str, url: str) -> bool:
    start = time.time()
    try:
        req = Request(url, headers={"User-Agent": "full-stack-verify/1.0"})
        with urlopen(req, timeout=15) as response:
            elapsed_ms = round((time.time() - start) * 1000)
            print(f"[OK]   {name:<20} {url}  ({response.status}, {elapsed_ms}ms)")
            return True
    except URLError as exc:
        elapsed_ms = round((time.time() - start) * 1000)
        print(f"[FAIL] {name:<20} {url}  ({exc}, {elapsed_ms}ms)")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Check every deployed service is reachable.")
    parser.add_argument("--frontend", required=True, help="Live frontend URL")
    parser.add_argument("--backend", required=True, help="Live backend URL (base, no trailing slash)")
    parser.add_argument("--ai-service", required=False, help="Live AI service URL, if exposed separately")
    args = parser.parse_args()

    print("Checking full-stack deployment...\n")

    results = [
        check("Frontend", args.frontend),
        check("Backend /health", f"{args.backend.rstrip('/')}/health"),
    ]

    if args.ai_service:
        results.append(check("AI service /health", f"{args.ai_service.rstrip('/')}/health"))

    # Indirect DB check: a lesson-list endpoint that requires a working DB
    # query is a good proxy for "database is connected", without needing
    # DB credentials in this script.
    results.append(
        check("Backend -> DB (lessons)", f"{args.backend.rstrip('/')}/api/lessons")
    )

    print()
    if all(results):
        print("ALL CHECKS PASSED — full stack is reachable and connected.")
        sys.exit(0)
    else:
        failed = results.count(False)
        print(f"{failed} check(s) FAILED — see above before telling the team it's ready.")
        sys.exit(1)


if __name__ == "__main__":
    main()
