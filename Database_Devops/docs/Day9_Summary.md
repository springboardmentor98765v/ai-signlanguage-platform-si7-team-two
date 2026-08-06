# Milestone 3 — Day 9 (Intern 5: Database & QA Engineer)

## Objectives & Tasks Completed

Day 9 focused on creating a comprehensive **Deployment Readiness Checklist** for Milestone 4, aligning hosting choices, environment configuration, database migration procedures, backup schedules, and monitoring requirements across all 5 team roles.

> [!NOTE]
> This is a planning document only. In accordance with Milestone 3 guidelines, no live cloud deployment or external infrastructure provisioning took place today.

---

## 1. Deliverables Created

- **Deployment Readiness Checklist Document:**
  - File Location: `docs/DEPLOYMENT_READINESS_CHECKLIST.md`
  - Explicitly tagged: **FOR MILESTONE 4 USE ONLY — PLANNING DOCUMENT**

---

## 2. Key Elements Outlined in the Checklist

1. **Hosting & Platform Selection:**
   - Frontend: Vercel (Free Hobby Tier)
   - Backend API: Render (Free Web Service Tier)
   - AI Model Service: Render Container / Hugging Face Spaces
   - Database: Neon Serverless PostgreSQL (Free Tier)
2. **Environment Variable & Secrets Protocol:**
   - Production connection strings (`DATABASE_URL`), cryptographically generated JWT secrets (`JWT_SECRET_KEY`), and restricted production CORS origin policies.
3. **Database Migration & Backup Strategy:**
   - Alembic single-head migration verification (`alembic upgrade head`).
   - Daily automated database snapshots (`pg_dump`) with 30-day retention.
   - Mandatory snapshot gate prior to executing any production schema migration.
4. **Security & Monitoring Readiness:**
   - Security header enforcement, TLS 1.2+ HTTPS mandatory redirects, and UptimeRobot HTTP `/health` probe monitoring.

---

## Checkpoints

- [x] Deployment Readiness Checklist document created (`docs/DEPLOYMENT_READINESS_CHECKLIST.md`)
- [x] Checklist reviewed with the whole team (Interns 1, 2, 3, 4, and 5)
- [x] Checklist clearly marked as 'for Milestone 4 use'
