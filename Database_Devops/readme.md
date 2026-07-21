# 🗄️ Database & DevOps — Intern 5

This directory contains all database infrastructure, schema definitions, seed data, datasets, backup/restore tooling, monitoring, deployment support, and frontend hosting configs for the **AI Sign Language Platform**.

**Milestone 2: Days 1–10 — All deliverables complete.**

---

## 📁 Directory Structure

```
Database_Devops/
├── db/                             # Database schema & migration files
│   ├── schema/
│   │   ├── 01-schema.sql           # PostgreSQL table definitions
│   │   └── 02-seed.sql             # Idempotent seed data
│   ├── models/                     # SQLAlchemy ORM models
│   ├── erd/
│   │   └── erd.mmd                 # Mermaid entity-relationship diagram
│   ├── DATA_MODEL.md               # Detailed data model documentation
│   └── README.md                   # DB-specific usage guide
│
├── datasets/                       # Training & validation datasets
│   ├── sign_dataset.csv            # Hand-landmark dataset (x0–z20 + label)
│   └── README.md                   # Column reference & usage guide
│
├── infra/                          # Infrastructure configuration
│   ├── docker-compose.db.yml       # Standalone Postgres container
│   └── docker-compose.yml          # Full-stack (backend + AI + DB)
│
├── ai-service/                     # AI service deployment scaffolding (Day 9)
│   ├── Dockerfile                  # Updated for trained model artifacts
│   ├── requirements.txt            # Placeholder — merge with Intern 3's
│   ├── app/                        # FastAPI prediction app
│   ├── models/                     # Drop .pkl model files here
│   └── docs/
│       ├── MODEL_CARD.md           # Placeholder for Intern 3's model card
│       └── ROBUSTNESS_TESTING.md   # Placeholder for robustness test results
│
├── backend/                        # Backend placeholder service
│   ├── Dockerfile
│   ├── app/
│   └── requirements.txt
│
├── frontend-hosting/               # Frontend hosting configs (Day 9)
│   ├── netlify.toml                # Netlify deployment config
│   └── vercel.json                 # Vercel deployment config
│
├── backup/                         # Database backup/restore system (Day 6)
│   ├── scripts/
│   │   ├── backup_db.py
│   │   └── restore_db.py
│   ├── backups/                    # Generated backup files
│   └── README.md
│
├── monitoring/                     # Uptime monitoring & testing (Day 8–10)
│   ├── scripts/
│   │   ├── check_uptime.py         # UptimeRobot-style health checks
│   │   ├── load_test.sh            # Basic load testing
│   │   ├── verify_full_stack.py    # Day 9: full-stack reachability check
│   │   └── smoke_test_full_journey.py  # Day 10: end-to-end learner journey
│   ├── results/
│   └── README.md
│
├── DEPLOYMENT_GUIDE.md             # Day 10: how to run/deploy this project
└── readme.md                       # ← You are here
```

---

## 🚀 Quick Start

### 1. Set up Environment Variables

Copy `.env.example` to `.env` at the root of the project and set a secure password for the database:

```bash
cp .env.example .env
# Edit .env and update DB_PASSWORD to a secure value
```

### 2. Stand up PostgreSQL locally (Day 2 Docker setup)

Use the provided docker-compose configuration. This will automatically run `01-schema.sql` and `02-seed.sql` on first startup:

```bash
docker compose --env-file .env -f Database_Devops/infra/docker-compose.db.yml up -d
```

### 3. Full-stack (Backend + AI + DB) via Docker Compose

```bash
docker compose --env-file .env -f Database_Devops/infra/docker-compose.yml up --build
```

---

## 🗃️ Database Schema Overview

| Table | Purpose |
|---|---|
| `users` | Registered platform users |
| `signs` | Sign language gesture definitions |
| `sessions` | User learning/practice sessions |
| `predictions` | Model inference results per frame |
| `raw_landmarks` | Raw MediaPipe hand landmark vectors |
| `feedback` | User-submitted gesture corrections |
| `lessons` | Structured sign language lessons (A–Z) |
| `assessments` | Practice assessments with sub-scores |
| `certificates` | Completion certificates |

> See [`db/DATA_MODEL.md`](db/DATA_MODEL.md) for full field-level documentation and the ERD at [`db/erd/erd.mmd`](db/erd/erd.mmd).

---

## 📊 Datasets

| File | Rows | Description |
|---|---|---|
| `sign_dataset.csv` | ~1000+ | 63 MediaPipe landmark coordinates (x0–z20) + gesture label |

**Landmark layout:** Each row contains `x0, y0, z0 ... x20, y20, z20` (21 hand landmarks × 3 axes) followed by a `label` column (e.g., `A`, `B`, `thumbs_up`).

> See [`datasets/README.md`](datasets/README.md) for full column reference.

---

## 🧪 Verification & Testing (Days 9–10)

### Full-Stack Reachability Check (Day 9)
```bash
python Database_Devops/monitoring/scripts/verify_full_stack.py \
    --frontend https://your-frontend.netlify.app \
    --backend https://your-backend.onrender.com
```

### End-to-End Learner Journey Smoke Test (Day 10)
```bash
python Database_Devops/monitoring/scripts/smoke_test_full_journey.py \
    --base-url https://your-backend.onrender.com
```

> See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for the full deployment & run guide.

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| Database | PostgreSQL 15 |
| ORM / Queries | Raw SQL + psycopg2 / SQLAlchemy |
| Containerization | Docker + Docker Compose |
| ERD Tooling | Mermaid.js |
| Dataset Format | CSV (MediaPipe landmarks) |
| Backup/Restore | Python + pg_dump / pg_restore |
| Monitoring | UptimeRobot + custom scripts |
| Frontend Hosting | Netlify / Vercel (free tier) |

---

## 📋 Milestone 2 Delivery Summary

| Day | Deliverable | Status |
|-----|-------------|--------|
| 1 | Schema planning & data model design | ✅ |
| 2 | Docker Postgres setup, seed data, certificates table | ✅ |
| 3 | Full-stack compose scaffolding | ✅ |
| 4–5 | Placeholder services, init schema sync | ✅ |
| 6 | Database backup/restore system | ✅ |
| 7 | Docker Compose M2 update, deployment notes | ✅ |
| 8 | Uptime monitoring & load testing | ✅ |
| 9 | AI service deployment scaffolding, frontend hosting configs, verify script | ✅ |
| 10 | End-to-end smoke test, deployment guide | ✅ |

---

## 👤 Intern 5 — Ownership

| Area | Owner |
|---|---|
| Schema design | Intern 5 (Database & DevOps) |
| Seed data | Intern 5 |
| Dataset curation | Intern 5 |
| Infra configs (Docker) | Intern 5 |
| Backup/Restore | Intern 5 |
| Monitoring & Load Testing | Intern 5 |
| Deployment support (Day 9–10) | Intern 5 |

---

## 🔗 Related Docs

- [`Backend/README.md`](../Backend/README.md) — FastAPI scaffolding that consumes this schema
- [`AIML_CV/README.md`](../AIML_CV/README.md) — Model that produces landmark data
- [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) — How to run/deploy this project
- Root [`README.md`](../README.md) — Project overview

---

*Last updated: Milestone 2, Day 10 — All Intern 5 deliverables complete*
