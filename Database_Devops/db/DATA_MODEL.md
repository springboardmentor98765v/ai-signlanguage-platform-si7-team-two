# Data Dictionary — Milestone 1

Draft for team review (SRS §6, Intern 5, Day 1). Every entity below maps to
a group named in the Day 1 task: Users/Roles, Lessons/Modules, Practice
Sessions, Assessments, Feedback, Analytics.

## roles
RBAC support for FR-2 ("enforce Role-Based Access Control").

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| name | varchar(30) unique | `Learner`, `Instructor`, `Trainer`, `Admin` |

## users
Backs FR-1 (Login/Register) and FR-2 (registration/login, JWT, RBAC).

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| role_id | uuid FK → roles.id | |
| full_name | varchar(120) | |
| email | varchar(255) unique | login identifier |
| password_hash | varchar(255) | **never plain text** — NFR "Security" |
| created_at / updated_at | timestamptz | audit |

## courses
Supports FR-2 ("CRUD APIs for Lessons/Modules").

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| name | varchar(120) | e.g. "Alphabet" |
| level | varchar(20) | Beginner/Intermediate/Advanced — matches Intern 1's Day 4 dashboard cards |
| description | text | |
| created_at | timestamptz | |

## lessons
The "Modules" in FR-2; one row per alphabet letter per Intern 2's Day 5 seed task.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| course_id | uuid FK → courses.id | |
| letter | varchar(2) | target sign, e.g. "A" |
| title | varchar(120) | |
| description | text | |
| reference_image_url | varchar(500) | shown on Practice screen (Intern 1 Day 5) |
| order_index | int | display order |
| created_at | timestamptz | |

## practice_sessions
Backs FR-4 ("create/track practice sessions").

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users.id | |
| lesson_id | uuid FK → lessons.id | |
| status | varchar(20) | `in_progress`, `completed`, `abandoned` |
| attempt_count | int default 0 | incremented per attempt |
| started_at | timestamptz | |
| ended_at | timestamptz nullable | null while in progress |

## assessments
Backs FR-3's output contract and FR-4's scoring. Field names deliberately
match Intern 3's stated Day 6 API response shape (`predicted_sign`,
`confidence`) so no translation layer is needed.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| session_id | uuid FK → practice_sessions.id | one session can have multiple attempts/assessments |
| predicted_sign | varchar(2) | from AI service |
| confidence | numeric(5,4) | 0.0000–1.0000, from AI service |
| expected_sign | varchar(2) | the lesson's target letter |
| accuracy_score | numeric(5,2) | 0–100, computed by Intern 4's scoring engine |
| created_at | timestamptz | |

## feedback
Backs FR-4's "rule-based feedback."

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| assessment_id | uuid FK → assessments.id | one assessment may yield several messages |
| category | varchar(30) | `hand_shape`, `timing`, `position`, `motion` — matches SRS Day 5 examples |
| message | text | human-readable correction |
| created_at | timestamptz | |

## learner_analytics
Backs FR-4's "aggregate basic analytics per learner" — one summary row per
user, recomputed as sessions complete.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| user_id | uuid FK → users.id, unique | one row per learner |
| average_accuracy | numeric(5,2) | |
| lessons_completed | int | |
| weak_letters | jsonb | array of letters below a threshold accuracy |
| updated_at | timestamptz | |

## Design decisions & assumptions
1. **UUID primary keys**, not auto-increment ints — assumption, not stated
   in the SRS. Chosen because Milestone 1's architecture is explicitly
   microservice-shaped (API Gateway, separate services per SRS §1.2), and
   UUIDs avoid ID collisions if any service ever generates records
   independently of the central DB. Flag for team review — a serial/bigint
   PK is equally valid for M1's scope and simpler to seed by hand if the
   team prefers.
2. **`assessments` is many-to-one with `practice_sessions`**, not 1:1 —
   assumption, based on `attempt_count` existing on the session (§6, Intern
   4 Day 3: "attempt count, duration timer"), implying a learner can retry
   within one session.
3. **`roles` as its own table** rather than an enum/string column on
   `users` — chosen for RBAC extensibility (FR-2 names 4 roles;
   Instructor/Trainer aren't used by any Day 1–7 flow but are named in the
   Frontend's role selector, SRS §6 Intern 1 Day 3).
4. **PostgreSQL dialect** assumed over MySQL — SRS §6 (Intern 5, Day 2)
   lists "PostgreSQL (or MySQL)" as a choice. Postgres is used here for
   `jsonb` (weak_letters) and native `uuid` generation. If the team prefers
   MySQL, `schema.sql` needs the noted swaps (see comments in that file).

## certificates
Stores a record every time a learner earns a certificate.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| learner_id | uuid FK -> users.id | |
| average_score | numeric | |
| lessons_completed | int default 0 | |
| certificate_code | varchar(64) unique | Human-shareable code |
| file_path | varchar(255) nullable | Path to generated PDF |
| issued_at | timestamptz | |
| is_valid | boolean default true | |

## recommendations
Holds suggestions for practice based on past performance.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | |
| learner_id | uuid FK -> users.id | |
| letter_or_word | varchar(50) | Which letter/word needs practice |
| reason | varchar(255) | Plain-language reason |
| recent_avg_accuracy | numeric nullable | The accuracy that triggered this |
| status | varchar(20) | active, completed, dismissed |
| created_at | timestamptz | |
| resolved_at | timestamptz nullable | |
