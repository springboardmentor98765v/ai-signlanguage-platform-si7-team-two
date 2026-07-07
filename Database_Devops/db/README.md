# Data Layer — Day 1 Deliverable

Owner: Intern 5. Task per SRS §6 (Intern 5, Day 1): draft an ER diagram
covering Users/Roles, Lessons/Modules, Practice Sessions, Assessments,
Feedback and Analytics records, for team review.

## Contents
- `erd/erd.mmd` — Mermaid ER diagram (render on GitHub, or paste into
  https://mermaid.live for a visual).
- `DATA_MODEL.md` — plain-English data dictionary: every entity, every
  field, every relationship, with the SRS section that justifies it.
- `schema/schema.sql` — the ERD translated into PostgreSQL DDL. **Draft
  only** — not executed against any database yet. This exists so Intern 2
  and Intern 4 can start writing ORM models/Pydantic schemas against real
  column names as soon as the ERD is approved, without waiting for Day 2's
  live instance.
- `schema/seed.sql` — draft seed data (roles, alphabet lessons A/B/C/L/Y
  matching Intern 3's SRS Day 4 sample letters). **Not run yet** — real
  seeding happens Day 5 (SRS §6, Intern 2 Day 5) once the schema is final
  and a live DB exists (Day 2).

## Review checklist for Interns 2 & 4 (please confirm by end of Day 1)
- [ ] Does `users`/`roles` support the RBAC roles needed for FR-2
      (Learner/Instructor/Trainer/Admin)?
- [ ] Does `assessments` carry the exact fields Intern 3's prediction
      service will return (`predicted_sign`, `confidence`) per FR-3?
- [ ] Does `practice_sessions` capture what Intern 4's scoring engine
      needs (attempt count, duration, status) per FR-4?
- [ ] Any missing fields for the Frontend's mock-to-real API swap (Day 6)?

Sign-off here unblocks Day 2 (live Postgres instance) and Day 3-4 (ORM
models), per the Dependency Matrix in SRS §5.
