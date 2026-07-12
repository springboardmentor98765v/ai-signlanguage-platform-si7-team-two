# Base Document Alignment (Data & Infrastructure Layer)

This maps the full-vision architecture document ("AI-Powered Sign Language
Learning & Assessment Platform" base doc) to what was actually built for
Milestone 1, and explains every place the two diverge on purpose. Read this
alongside `DATA_MODEL.md` (the schema itself) and the root SRS (the binding
M1 requirements).

## Why two documents disagree, and which one wins for M1

The base document describes the **eventual full product** (cloud
deployment, 5 separate databases, certificates, payment gateway, advanced
analytics/recommendations, email/notification services). The SRS explicitly
scopes Milestone 1 down to a minimal end-to-end skeleton (§1.3–1.4) and
lists most of the base doc's grander features as **out of scope for M1**.
Wherever the two conflict, the SRS wins for anything Day 1–7 — the base doc
is background/vision context, not a second set of binding requirements.

## 1. Data Layer: 5 databases (base doc) → 1 shared database (SRS FR-5)

| Base doc's "Data Layer" box | Implemented as (this repo) |
|---|---|
| User Database | `roles`, `users` tables |
| Learning Database | `courses`, `lessons` tables |
| Assessment Database | `practice_sessions`, `assessments`, `feedback` tables |
| Analytics Database | `learner_analytics` table |
| Media Storage | `lessons.reference_image_url` (a plain URL column — no object storage service; SRS §1.4 lists cloud storage integration as out of scope for M1) |

All five live as tables inside the **one** Postgres instance stood up in
Day 2, per SRS FR-5's explicit wording ("a shared database"). Splitting
into 5 physical databases/microservices-per-service is real future work,
not an M1 oversight — the SRS's own day-wise plan never asks for it within
Days 1–7.

## 2. Role naming discrepancy — needs a team decision, not a code fix

- Base doc: `Learner`, `Instructor`, `Accessibility Trainer`, `Administrator`
- SRS (FR-2, and Intern 2's Day 3 task text, verbatim): `Learner`,
  `Instructor`, `Trainer`, `Admin`

`db/schema/seed.sql` currently seeds the SRS's short form (`Trainer`,
`Admin`) since that's the literal wording in your graded requirements doc.
**Action item for the team, not a schema bug:** confirm with your mentor
whether the long form should replace it before Intern 2 builds RBAC
decorators against one spelling on Day 4 — renaming a seeded role value
later is a one-line `UPDATE`, but is cleaner to settle now.

## 3. Assessment sub-scores (base doc Step 7) — deferred past M1 on purpose

The base doc's Assessment Engine walkthrough scores 5 separate parameters
(hand shape, finger position, timing, motion, position) that combine into
one overall accuracy. `assessments.accuracy_score` in this schema stores
only the **final combined number**, with no columns for the 5 sub-scores.

This is intentional: SRS FR-3 (Intern 3's actual Day 1-7 AI service scope)
only ever returns `{predicted_sign, confidence}` — a single classification
output, not per-parameter pose analysis. There is no upstream data source
in M1 to populate 5 sub-score columns with. Adding them now would be
speculative schema bloat for a data source that doesn't exist yet.

**If a later milestone adds per-parameter pose scoring:** extend
`assessments` with nullable columns (`hand_shape_score`,
`finger_position_score`, `timing_score`, `motion_score`,
`position_score`) via a proper migration at that time — don't add them
speculatively now.

## 4. Explicitly out of scope for M1 (confirmed absent from this schema, on purpose)

Per SRS §1.4, none of the following exist in `db/schema/schema.sql`, and
that is correct for Day 1–7:
- Certificates (base doc Outcome 6) — no `certificates` table.
- Payment gateway (base doc's "External Services" box) — no `payments` table.
- Advanced analytics / personalized recommendations (base doc Steps 8–9;
  e.g. "Improvement Rate," "Recommended Lessons") — `learner_analytics`
  only carries the 3 fields SRS Day 6 (Intern 4) actually asks for
  (`average_accuracy`, `lessons_completed`, `weak_letters`). Do not add
  `improvement_rate` or `recommended_lessons` columns for M1 — SRS §1.4
  names "advanced analytics/recommendations" as explicitly deferred.
- Email/notification services (SendGrid/FCM in base doc) — no related
  tables or env vars beyond what Days 1–7 need.
- Multi-cloud infra (AWS/Azure, autoscaling, Prometheus/Grafana, backup &
  disaster recovery) — `infra/` only has the Day 2 database container and
  will only gain Day 5/6's Docker Compose + CI stub, never cloud deploy
  configs, within this milestone.

## Bottom line
Day 1's ER diagram and Day 2's running database match the SRS exactly, and
every visible gap against the fuller base document is a deliberate,
documented M1 scope boundary — not a missed requirement.
