-- ============================================================
-- Milestone 2 — Draft Schema Addition (Day 1 deliverable)
-- Owner: Intern 5 (Data Layer)
-- Status: DRAFT — for team review. NOT executed against any
-- database yet. Execution is M2 Day 2 (SRS M2 §7, Intern 5, Day 2:
-- "create the new Certificates and Recommendations tables"), plus
-- Day 3 for the Instructor-Student mapping table.
--
-- This ADDS to the existing Milestone 1 schema (db/schema/schema.sql) —
-- it does not replace or restate it. All 8 Milestone 1 tables remain
-- unchanged today.
-- ============================================================

CREATE TABLE certificates (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id               UUID NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    score_achieved          NUMERIC(5,2) NOT NULL CHECK (score_achieved BETWEEN 0 AND 100),
    issued_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    certificate_file_path   VARCHAR(500),
    UNIQUE (user_id, course_id)
);

CREATE INDEX idx_certificates_user_id ON certificates(user_id);

CREATE TABLE recommendations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id   UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    reason      VARCHAR(255),
    status      VARCHAR(20) NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'completed', 'dismissed')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);

-- NOTE: instructor_id/student_id are both FKs into the same `users` table.
-- Restricting instructor_id to users with the Instructor role (and
-- student_id to Learners) is proposed to be enforced at the application
-- layer (Intern 2's API), not via a DB constraint — Postgres CHECK
-- constraints can't easily reference another table's column inline.
CREATE TABLE instructor_student_links (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instructor_id   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    student_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (instructor_id, student_id)
);

CREATE INDEX idx_instructor_links_instructor_id ON instructor_student_links(instructor_id);
CREATE INDEX idx_instructor_links_student_id ON instructor_student_links(student_id);

-- Deliberately separate from the existing `learner_analytics` table
-- (a lifetime running summary, unchanged by Milestone 2). This is a new,
-- week-scoped snapshot: one row per learner per week.
CREATE TABLE weekly_analytics (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    week_start_date     DATE NOT NULL,
    average_accuracy    NUMERIC(5,2) NOT NULL DEFAULT 0,
    lessons_practiced   INT NOT NULL DEFAULT 0,
    improvement_rate    NUMERIC(5,2),
    weak_letters        JSONB NOT NULL DEFAULT '[]',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, week_start_date)
);

CREATE INDEX idx_weekly_analytics_user_id ON weekly_analytics(user_id);
