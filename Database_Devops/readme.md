# 🗄️ Database & DevOps — Intern 5

This directory contains all database infrastructure, schema definitions, seed data, and datasets for the **AI Sign Language Platform**.

---

## 📁 Directory Structure

```
Database_Devops/
├── db/                         # Database schema & migration files
│   ├── schema/
│   │   ├── 01-schema.sql       # PostgreSQL table definitions
│   │   └── 02-seed.sql         # Idempotent seed data
│   ├── erd/
│   │   └── erd.mmd             # Mermaid entity-relationship diagram
│   ├── DATA_MODEL.md           # Detailed data model documentation
│   └── README.md               # DB-specific usage guide
│
├── datasets/                   # Training & validation datasets
│   ├── sign_dataset.csv        # Hand-landmark dataset (x0–z20 + label)
│   └── README.md               # Column reference & usage guide
│
├── infra/                      # Infrastructure configuration (WIP)
│   └── README.md               # Infrastructure setup notes
│
└── readme.md                   # ← You are here
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

> See [`db/DATA_MODEL.md`](db/DATA_MODEL.md) for full field-level documentation and the ERD at [`db/erd/erd.mmd`](db/erd/erd.mmd).

---

## 📊 Datasets

| File | Rows | Description |
|---|---|---|
| `sign_dataset.csv` | ~1000+ | 63 MediaPipe landmark coordinates (x0–z20) + gesture label |

**Landmark layout:** Each row contains `x0, y0, z0 ... x20, y20, z20` (21 hand landmarks × 3 axes) followed by a `label` column (e.g., `A`, `B`, `thumbs_up`).

> See [`datasets/README.md`](datasets/README.md) for full column reference.

---

## 🔧 Tech Stack

| Component | Technology |
|---|---|
| Database | PostgreSQL 15 |
| ORM / Queries | Raw SQL + psycopg2 (Backend) |
| Containerization | Docker |
| ERD Tooling | Mermaid.js |
| Dataset Format | CSV (MediaPipe landmarks) |

---

## 👤 Intern 5 — Ownership

| Area | Owner |
|---|---|
| Schema design | Intern 5 (Database & DevOps) |
| Seed data | Intern 5 |
| Dataset curation | Intern 5 |
| Infra configs | Intern 5 (In Progress) |

---

## 🔗 Related Docs

- [`Backend/README.md`](../Backend/README.md) — FastAPI scaffolding that consumes this schema
- [`AIML_CV/README.md`](../AIML_CV/README.md) — Model that produces landmark data
- Root [`README.md`](../README.md) — Project overview

---

*Last updated: Day 1 — Database & DevOps setup phase*
