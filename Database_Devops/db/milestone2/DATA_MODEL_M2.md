# Milestone 2 — New Tables/Fields Plan (Day 1 Deliverable)

Checkpoint: *"List of new tables/fields written down"* (SRS M2 §7, Intern
5, Day 1). Four new entities, matching FR-5 exactly: *"persist all new
Milestone 2 data (certificates, recommendations, instructor-student links,
weekly stats)."*

## 1. certificates
Backs FR-4 (certificate issuance) and the M2 acceptance criterion *"a
qualifying learner can download a real certificate PDF"* (§9.2).

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users.id | the learner who earned it |
| course_id | uuid FK → courses.id | which course was completed |
| score_achieved | numeric(5,2) | the qualifying average score at issue time |
| issued_at | timestamptz | |
| certificate_file_path | varchar(500) | where the generated PDF lives (Intern 4 generates the file via ReportLab/pdf-lib; this column just stores the path/URL) |

Assumption (flag for Intern 4's Day 6 sign-off): one certificate per
`(user_id, course_id)` pair — a learner earns one certificate per course,
not one per lesson. Unique constraint on `(user_id, course_id)` proposed
below.

## 2. recommendations
Backs FR-4's recommendation engine and the acceptance criterion *"if
they're struggling, a practice recommendation"* (§9.2).

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users.id | who the recommendation is for |
| lesson_id | uuid FK → lessons.id | which letter/lesson to practice more |
| reason | varchar(255) | short human-readable reason, e.g. "below 70% in last 3 attempts" |
| status | varchar(20) | `active` \| `completed` \| `dismissed` |
| created_at | timestamptz | |

## 3. instructor_student_links
Backs FR-2's Instructor-Student mapping and the M2 dependency-matrix item
*"Instructor-Student & Certificate tables (Intern 5) → Backend APIs, by
Day 3-4."*

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| instructor_id | uuid FK → users.id | must hold the `Instructor` role — enforced at the application layer, not a DB constraint (Postgres can't easily check a FK's role inline) |
| student_id | uuid FK → users.id | must hold the `Learner` role, same caveat |
| assigned_at | timestamptz | |

Unique constraint on `(instructor_id, student_id)` proposed, to prevent
duplicate assignments.

## 4. weekly_analytics
Backs FR-4's weekly analytics and FR-5's "weekly stats." **Deliberately
separate from the existing `learner_analytics` table** — that table is a
lifetime running summary (unchanged in M2); this is a new, week-scoped
snapshot, one row per learner per week.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users.id | |
| week_start_date | date | identifies which week (e.g. the Monday of that week) |
| average_accuracy | numeric(5,2) | that week's average |
| lessons_practiced | int | count of distinct lessons practiced that week |
| improvement_rate | numeric(5,2) | change vs. the previous week — nullable, since week 1 has no prior week to compare against |
| weak_letters | jsonb | that week's weak-letter list |
| created_at | timestamptz | |

Unique constraint on `(user_id, week_start_date)` proposed, so recomputing
a week overwrites rather than duplicates.

## Explicitly NOT part of Day 1 (coming later per the SRS day plan)
- `lessons.category` / `lessons.difficulty` — M2 Day 3 (Intern 2 +
  Intern 5 joint task per the SRS Day 3 row).
- `assessments.possible_issue` — needed by M2 Day 7 once Intern 3's
  error-type hint exists; noted here for awareness, not built today.
