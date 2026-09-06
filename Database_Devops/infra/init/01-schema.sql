-- ============================================================
-- NOTE: this file is a COPY of db/schema/schema.sql, placed here
-- because Postgres's official image auto-runs every .sql file in
-- /docker-entrypoint-initdb.d (alphabetically) on first container
-- start. db/schema/schema.sql remains the reviewed source of truth
-- for team sign-off; keep this copy in sync until Day 3/4 introduces
-- a proper migration tool.
-- ============================================================

-- ============================================================
-- Milestone 1 — Draft Schema (Day 1 deliverable)
-- Owner: Intern 5 (Data Layer)
-- Status: DRAFT — for team review. NOT executed against any
-- database yet. Execution against a live Postgres instance is
-- a Day 2 task (SRS §6, Intern 5, Day 2).
--
-- Dialect: PostgreSQL 14+
-- If the team chooses MySQL instead (SRS §6 allows either):
--   - replace `uuid` + `gen_random_uuid()` with CHAR(36) + UUID()
--   - replace `jsonb` with JSON
--   - replace `timestamptz` with DATETIME
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- for gen_random_uuid()

-- ---------- roles ----------
CREATE TABLE roles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(30) NOT NULL UNIQUE
);

-- ---------- users ----------
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id         UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    full_name       VARCHAR(120) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    mascot_id       VARCHAR(50) DEFAULT 'owl',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_role_id ON users(role_id);

-- ---------- courses ----------
CREATE TABLE courses (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(120) NOT NULL,
    level       VARCHAR(20) NOT NULL
                    CHECK (level IN ('Beginner', 'Intermediate', 'Advanced')),
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- lessons ----------
CREATE TABLE lessons (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id           UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    letter              VARCHAR(2) NOT NULL,
    title               VARCHAR(120) NOT NULL,
    description         TEXT,
    reference_image_url VARCHAR(500),
    order_index         INT NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_lessons_course_id ON lessons(course_id);

-- ---------- practice_sessions ----------
CREATE TABLE practice_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id       UUID NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
    status          VARCHAR(20) NOT NULL DEFAULT 'in_progress'
                        CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    attempt_count   INT NOT NULL DEFAULT 0,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at        TIMESTAMPTZ
);

CREATE INDEX idx_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_sessions_lesson_id ON practice_sessions(lesson_id);

-- ---------- assessments ----------
CREATE TABLE assessments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES practice_sessions(id) ON DELETE CASCADE,
    predicted_sign  VARCHAR(2) NOT NULL,
    confidence      NUMERIC(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    expected_sign   VARCHAR(2) NOT NULL,
    hand_shape_score NUMERIC(5,2) NOT NULL,
    finger_position_score NUMERIC(5,2) NOT NULL,
    timing_score    NUMERIC(5,2) NOT NULL,
    motion_score    NUMERIC(5,2) NOT NULL,
    position_score  NUMERIC(5,2) NOT NULL,
    overall_score   NUMERIC(5,2) NOT NULL CHECK (overall_score BETWEEN 0 AND 100),
    is_correct      BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_assessments_session_id ON assessments(session_id);

-- ---------- feedback ----------
CREATE TABLE feedback (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    category        VARCHAR(30) NOT NULL
                        CHECK (category IN ('hand_shape', 'timing', 'position', 'motion')),
    severity        VARCHAR(20) NOT NULL DEFAULT 'moderate',
    message         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_feedback_assessment_id ON feedback(assessment_id);

-- ---------- learner_analytics ----------
CREATE TABLE learner_analytics (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    average_accuracy    NUMERIC(5,2) NOT NULL DEFAULT 0,
    lessons_completed   INT NOT NULL DEFAULT 0,
    weak_letters        JSONB NOT NULL DEFAULT '[]',
    total_practice_time INT NOT NULL DEFAULT 0,
    last_updated        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------- lesson_progress ----------
CREATE TABLE IF NOT EXISTS lesson_progress (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id           UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    stars               INT NOT NULL DEFAULT 0,
    highest_accuracy    NUMERIC(5,2) NOT NULL DEFAULT 0,
    is_completed        BOOLEAN NOT NULL DEFAULT false,
    is_unlocked         BOOLEAN NOT NULL DEFAULT false,
    completed_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_lesson_progress_user_lesson UNIQUE (user_id, lesson_id)
);

CREATE INDEX idx_lesson_progress_user_id ON lesson_progress(user_id);
CREATE INDEX idx_lesson_progress_lesson_id ON lesson_progress(lesson_id);
