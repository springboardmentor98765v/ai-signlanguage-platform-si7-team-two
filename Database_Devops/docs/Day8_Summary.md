# Milestone 3 — Day 8 (Intern 5: Database & QA Engineer)

## Objectives & Tasks Completed

Day 8 focused on working with **Intern 2 (Backend)** to address and remediate security vulnerabilities identified during Day 7's OWASP ZAP baseline scan, re-running security scans, and conducting comprehensive data integrity checks across the database.

---

## 1. Security Issues Remediation (Joint Work with Intern 2)

- **Missing Security Headers Fixed:**
  - Added HTTP Security Headers to FastAPI (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`, `Content-Security-Policy`).
- **CORS Configuration Hardened:**
  - Replaced wildcard CORS origins (`*`) with explicit trusted local frontend origins (`http://localhost:3000`, `http://localhost:3001`).
- **Auth Endpoint Rate Limiting:**
  - Implemented per-IP rate-limiting middleware (max 10 login requests per minute) to prevent brute-force attacks.
- **Server Information Disclosure Suppressed:**
  - Suppressed default `Server: uvicorn` header to prevent technology stack fingerprinting.

---

## 2. Security Scan Re-test

- **Executed Command:**
  ```bash
  ./security/run_zap_baseline_scan.sh http://localhost:8001
  ```
- **Outcome:** **PASS** — **0 High Risk**, **0 Medium Risk** vulnerabilities remaining.
- **Documentation:** Updated `docs/ZAP_Findings_Review_Template.md` with full triage matrix and resolution sign-offs.

---

## 3. Data Integrity & Schema Audit

- **Foreign Key Constraints:** Confirmed `ON DELETE CASCADE` integrity across all relational models (`User` ➔ `Streak`, `Badge`, `Notification`).
- **User Activation Status (`is_active`):** Validated default value `TRUE` and boolean integrity across Alembic migration `0007_add_is_active_to_users` and PostgreSQL base schemas (`01-schema.sql`, `infra/init/01-schema.sql`).
- **UUID Default Integrity:** Verified `server_default=sa.text("gen_random_uuid()")` across all tables, ensuring PostgreSQL UUID generation succeeds without string-casting errors.
- **Zero Orphaned Records:** Verified database state after test runs — no dangling records exist for deleted users.

---

## Checkpoints

- [x] Critical security issues fixed together with Intern 2
- [x] Security scan re-run to confirm fixes (OWASP ZAP baseline scan passed)
- [x] Data integrity re-checked after security fixes
- [x] Triage report updated in `docs/ZAP_Findings_Review_Template.md`
