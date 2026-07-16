# Milestone 1 Database Review (M2 Day 1 Checkpoint)

Checkpoint: *"Milestone 1 database reviewed for what already exists"* (SRS
M2 §7, Intern 5, Day 1). Summarised here so Intern 2 and Intern 4 don't
need to re-read the full Milestone 1 documentation to sign off on the
Milestone 2 plan below.

## What already exists (8 tables, all live since M1 Day 2, ORM+migrations since Day 3/4)

| Table | Purpose | Relevant M2 touchpoint |
|---|---|---|
| `roles` | RBAC roles (Learner, Instructor, Trainer, Admin) | Instructor/Admin roles now become functionally active in M2 (dashboards, user management) |
| `users` | Accounts, auth, role assignment | Gains Profile/password-reset APIs (Intern 2); becomes the `instructor`/`student` side of the new mapping table |
| `courses` | Course groupings (e.g. "Alphabet") | Unchanged in M2 Day 1; may gain more courses as the lesson catalogue expands (Intern 2, Day 5) |
| `lessons` | One row per target sign | Gains `category` and `difficulty` fields — **M2 Day 3 work, not Day 1** |
| `practice_sessions` | Practice attempt tracking | Unchanged structurally; volume grows with the bigger letter set |
| `assessments` | AI prediction + score per attempt | Gains a `possible_issue` field to carry Intern 3's new error-type hint — **M2 Day 3 work** (Assessment table touch), noted here for awareness only |
| `feedback` | Rule-based correction messages | Expands with more rules (Intern 4's scope, not schema-affecting) |
| `learner_analytics` | Lifetime running summary per learner (average accuracy, lessons completed, weak letters) | Stays as-is — M2 introduces a **separate, week-scoped** table alongside it (see below); this table is not being replaced |

## What M1 deliberately deferred (per `db/BASE_DOCUMENT_ALIGNMENT.md`)

M1's alignment note explicitly flagged *"advanced analytics/recommendations"*
as out of scope for Milestone 1, per SRS M1 §1.4. Milestone 2's FR-4/FR-5
now explicitly bring exactly that into scope — the Recommendations and
Weekly Analytics tables below are that deferred work arriving on schedule,
not scope creep.

## Confirmed NOT changing on M2 Day 1

No existing table's columns change today, and no new table is created
against the live database today — this is the planning/review step. DDL
execution is M2 Day 2 (`db/milestone2/schema_m2_draft.sql` below is a
*draft* for review, same pattern as M1 Day 1's `schema.sql` draft).
