# Milestone 2 — Data Layer, Day 1

Owner: Intern 5. Task per SRS M2 §7 (Intern 5, Day 1): *"Review the
Milestone 1 database and setup, and plan the new tables/services needed:
Certificates, Recommendations, Instructor-Student mapping, and Weekly
Analytics."*

Same planning-only pattern as Milestone 1's Day 1 — nothing here is
executed against the live database yet. Execution is Day 2 (Certificates,
Recommendations) and Day 3 (Instructor-Student links, Lessons updates).

## Contents
- `EXISTING_SYSTEM_REVIEW.md` — what already exists from Milestone 1, and
  exactly which parts M2 touches vs. leaves alone. Covers the *"Milestone
  1 database reviewed"* checkpoint.
- `DATA_MODEL_M2.md` — the *"list of new tables/fields"* checkpoint: full
  data dictionary for all 4 new entities, with assumptions flagged for
  sign-off.
- `erd_m2_draft.mmd` — draft ERD extending `db/erd/erd.mmd` with the 4 new
  entities and their relationships to existing tables.
- `schema_m2_draft.sql` — draft DDL for the 4 new tables (review only, same
  role as M1 Day 1's `schema.sql` draft — gives Intern 2/4 real column
  names to plan against before Day 2's execution).

## Review checklist for Intern 2 & Intern 4 (per SRS M2 §7, Day 1: "plan
shared with Intern 2 and Intern 4 for sign-off")
- [ ] Does `instructor_student_links` give Intern 2 what's needed for the
      Day 3 Instructor-Student APIs (assign a student, fetch a student
      list)?
- [ ] Does `certificates` carry what Intern 4's Day 6-7 certificate logic
      needs (eligibility check inputs, file path for the generated PDF)?
- [ ] Does `recommendations` support Intern 4's Day 4 recommendation rule
      ("below 70% in the last 3 attempts")? Note: the rule's *evaluation
      logic* lives in Intern 4's service — this table only stores the
      *result*.
- [ ] Is `weekly_analytics` being correctly understood as **separate**
      from the existing `learner_analytics` (lifetime) table, not a
      replacement for it?
- [ ] Any fields missing for the Frontend's dashboards (Intern 1, Days
      4-6) to display this data once real APIs exist (M2 Day 9)?

Sign-off here unblocks Day 2 (Certificates + Recommendations tables live)
and Day 3 (Instructor-Student links + Lessons category/difficulty), per
the M2 Dependency Matrix (SRS M2 §6: *"Instructor-Student & Certificate
tables → Backend APIs, by Day 3-4"*).

## Note on `db/BASE_DOCUMENT_ALIGNMENT.md`
Milestone 1's alignment note flagged "advanced analytics/recommendations"
as deliberately deferred past M1 (SRS M1 §1.4). `recommendations` and
`weekly_analytics` here are that deferred scope arriving in Milestone 2 as
originally planned — worth a quick read of that note if anyone reviewing
this is wondering why M1's schema didn't already have these.
