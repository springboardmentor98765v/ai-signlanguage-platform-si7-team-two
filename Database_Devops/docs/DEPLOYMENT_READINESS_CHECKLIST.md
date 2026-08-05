# 🚀 Deployment Readiness Checklist (Milestone 4 Planning)

> [!IMPORTANT]
> **FOR MILESTONE 4 USE ONLY — PLANNING DOCUMENT ONLY**  
> *No deployment operations or live cloud provisioning take place in Milestone 3. All items in this checklist serve as the blueprint and requirements gate for putting the Sign Language Platform live in Milestone 4.*

---

## Document Control & Team Roles

- **Target Deployment Milestone:** Milestone 4
- **Document Version:** 1.0 (Prepared in Milestone 3, Day 9)
- **Primary Owner:** Intern 5 (Database, DevOps & QA Lead)
- **Team Reviewers:**
  - Intern 1: Frontend Developer (UI/UX & Web Deployment)
  - Intern 2: Backend Developer (API, Auth & Microservices)
  - Intern 3: AI/ML Engineer (Sign Recognition Model & Inference Service)
  - Intern 4: Product & Feature Lead (Assessments, Analytics & Notifications)
  - Intern 5: DB & DevOps Engineer (Database, Docker, CI/CD & Security)

---

## 1. Hosting & Infrastructure Selection Matrix

| Service Tier | Preferred Host / Platform | Backup Option | Resource Allocation / Tier | Cost | Target Deployment Domain / URL |
|---|---|---|---|---|---|
| **Frontend Application** | Vercel | Netlify | Free Tier / Hobby | $0/mo | `https://sign-language-app.vercel.app` |
| **Backend API Service** | Render | Railway / Fly.io | Free Web Service (FastAPI / Uvicorn) | $0/mo | `https://api-sign-language.onrender.com` |
| **AI / Inference Service** | Render | Hugging Face Spaces | Containerized Python 3.10 Service | $0/mo | `https://ai-sign-language.onrender.com` |
| **Database (PostgreSQL)** | Neon (Serverless Postgres) | Supabase / Render Postgres | Managed Postgres 15+ with SSL | $0/mo | `postgresql://...neon.tech/main_db` |

---

## 2. Production Environment Variables & Secrets Gate

> [!CAUTION]
> All production secrets must be securely configured in host provider environment dashboards and NEVER committed to source control.

- [ ] **Database Connection (`DATABASE_URL`):**
  - Set production PostgreSQL SSL connection string (`sslmode=require`).
  - Isolate production DB credentials from development/testing databases.
- [ ] **JWT Authentication Secrets:**
  - Generate strong 256-bit cryptographically secure `JWT_SECRET_KEY` (`openssl rand -hex 32`).
  - Set token expiration times (`ACCESS_TOKEN_EXPIRE_MINUTES=60`, `REFRESH_TOKEN_EXPIRE_DAYS=7`).
- [ ] **Cross-Origin Resource Sharing (`CORS_ORIGINS`):**
  - Set strict production CORS allowed origins matching the deployed frontend domain:
    `CORS_ORIGINS=["https://sign-language-app.vercel.app"]`
- [ ] **AI Inference Service API URL:**
  - Set `AI_SERVICE_URL` in backend environment pointing to production AI model endpoint.

---

## 3. Database Migration & Schema Readiness

- [ ] **Alembic Migration Verification:**
  - Run `alembic heads` locally to ensure a single clean migration lineage (`0007_add_is_active_to_users`).
  - Ensure zero unresolved migration branches or split heads.
- [ ] **Production Migration Strategy:**
  - Configure automated pre-deployment migration script in CI/CD pipeline (`alembic upgrade head`).
- [ ] **Initial Production Seed Data:**
  - Prepare minimal initial seed script for system roles, initial lessons, and default badges (`python db/seed_production.py`).
- [ ] **Database Connection Pooling:**
  - Configure SQLAlchemy connection pool settings for production serverless limits (`pool_size=5`, `max_overflow=10`, `pool_recycle=1800`).

---

## 4. Security Hardening & Compliance Checklist

- [ ] **HTTPS / SSL Enforcement:**
  - Verify TLS 1.2+ certificate auto-renewal on Vercel and Render.
  - Enforce `HTTP` to `HTTPS` redirect rules across all endpoints.
- [ ] **Security Headers:**
  - Enable production security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy`.
- [ ] **Rate Limiting & DDoS Protection:**
  - Enable per-IP rate limiting on auth (`/auth/login`, `/auth/register`) and practice endpoints.
- [ ] **OWASP ZAP Final Production Scan:**
  - Schedule baseline security scan against staging/production preview URLs before official release.

---

## 5. Automated Backup & Disaster Recovery Schedule

- [ ] **Automated Daily Database Backups:**
  - Configure daily automated PostgreSQL pg_dump snapshot at 02:00 UTC.
  - Store backups in secure S3-compatible cloud storage with 30-day retention policy.
- [ ] **Pre-Deployment Backup Standard:**
  - Require manual database snapshot before running any Alembic migration in production.
- [ ] **Restoration Verification:**
  - Document and test automated database restore workflow (`python backup/restore_db.py <snapshot_file>`).

---

## 6. Monitoring, Health Checks & Alerting

- [ ] **API Health Endpoint:**
  - Verify `/health` endpoint returns JSON status `{ "status": "healthy", "database": "connected" }`.
- [ ] **External Uptime Monitoring:**
  - Configure free UptimeRobot / BetterStack monitors hitting `/health` every 5 minutes.
  - Configure immediate email/Slack alerts on downtime or >2000ms latency.
- [ ] **Log Retention & Error Tracking:**
  - Enable structured JSON logging on FastAPI backend.
  - Integrate Sentry / Logtail free tier for real-time frontend and backend uncaught exception alerts.

---

## 7. Milestone 4 Go-Live Execution Order

```
[Phase 1: DB] Provision Neon Postgres ➔ Run Alembic Upgrade Head ➔ Load Production Seed Data
     │
[Phase 2: AI] Deploy AI Inference Container to Render ➔ Verify /health
     │
[Phase 3: Backend] Deploy FastAPI Service to Render ➔ Inject Env Vars ➔ Test /docs & Auth
     │
[Phase 4: Frontend] Deploy React App to Vercel ➔ Point API URL to Render Backend ➔ E2E Verification
     │
[Phase 5: Sign-off] Run Full Smoke Test Suite ➔ Activate UptimeRobot Monitoring ➔ Platform Live!
```

---

## Team Sign-off (Milestone 3, Day 9 Review)

- [x] **Intern 1 (Frontend):** Reviewed & Approved
- [x] **Intern 2 (Backend):** Reviewed & Approved
- [x] **Intern 3 (AI/ML):** Reviewed & Approved
- [x] **Intern 4 (Analytics/Features):** Reviewed & Approved
- [x] **Intern 5 (DB & DevOps Lead):** Prepared & Approved
