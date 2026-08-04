# OWASP ZAP Baseline Scan — Findings Review & Remediation (Day 7 / Day 8)

This document details the security triage and remediation results for the OWASP ZAP baseline scan executed against the local Docker Compose test stack (`docker-compose.test.yml`).

---

## Scan & Environment Details
- **Target URL:** `http://localhost:8001` (Local FastAPI backend)
- **Scan Tool:** OWASP ZAP Baseline Scan Docker (`owasp/zap2docker-stable:zap-baseline.py`)
- **Execution Date:** Milestone 3, Day 7 / Day 8
- **Scope:** Local Docker test environment only (no public/production endpoints touched)

---

## Security Findings & Triage Matrix

| Risk Level | Alert / Vulnerability Name | Affected Endpoint(s) | Root Cause | Owner | Fix Action / Status | Verification |
|---|---|---|---|---|---|---|
| **Medium** | Missing Security Headers (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`) | All API endpoints (`/`, `/auth/*`, `/practice/*`) | FastAPI backend lacked explicit security header middleware. | **Intern 2** (Backend) | Added custom ASGI Security Header Middleware emitting `nosniff`, `DENY`, and CSP headers. | **VERIFIED** (Re-scan clean) |
| **Medium** | CORS Wildcard Configuration | `/auth/login`, `/auth/register` | `CORSMiddleware` allowed `allow_origins=["*"]` on authenticated routes. | **Intern 2** (Backend) | Restricted origins to trusted local frontend origins (`http://localhost:3000`, `http://localhost:3001`). | **VERIFIED** (Re-scan clean) |
| **Low** | Missing Cookie Flags (`HttpOnly`, `Secure`, `SameSite`) | Session / Token cookie endpoints | Auth cookies missing explicit security attributes. | **Intern 2** (Backend) | Set `httponly=True`, `samesite="lax"`, and `secure=False` for local HTTP / `True` for HTTPS. | **VERIFIED** |
| **Low** | Server Banner Disclosure (`uvicorn` header) | All HTTP responses | Default Uvicorn response header reveals backend tech stack. | **Intern 5** (DB/DevOps) | Suppressed `Server` header in Uvicorn startup configuration (`--no-server-header`). | **VERIFIED** |
| **Informational** | Missing Rate Limiting on Auth Routes | `/auth/login`, `/auth/register` | Unthrottled login endpoint susceptible to brute-force attempts. | **Intern 2** / **Intern 5** | Implemented per-IP rate limiting middleware (10 req/min for auth routes). | **VERIFIED** |

---

## Day 8 Security & Data Integrity Verification

### 1. Security Scan Re-test Result
- **Command:** `./security/run_zap_baseline_scan.sh http://localhost:8001`
- **Result:** **0 High Risk**, **0 Medium Risk**, **0 Unaddressed Low Risk** findings.
- **Report Location:** `zap-reports/zap_baseline_report.html`

### 2. Data Integrity Audit Result
- **Foreign Key Constraints:** Verified `ON DELETE CASCADE` behavior across `users` ➔ `streaks`, `badges`, `notifications`.
- **`is_active` User Status Column:** Default `TRUE` verified across schema, Alembic migration `0007_add_is_active_to_users`, and ORM model (`User.is_active`).
- **UUID Default Verification:** Checked `server_default=sa.text("gen_random_uuid()")` across all tables to ensure zero syntax or type casting errors in PostgreSQL.
- **Orphan Cleanup:** Query run against `sign_language_db_test` confirmed zero orphaned notification or streak records.

---

## Sign-off & Completion

- [x] Scan run and report saved to `zap-reports/`
- [x] All High/Medium findings listed above and assigned an owner
- [x] Security headers and CORS policy hardened in local backend
- [x] Security scan re-run — zero critical/high risk issues remain
- [x] Data integrity re-checked after security fixes — all constraints intact
