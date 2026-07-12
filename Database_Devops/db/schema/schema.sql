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
    accuracy_score  NUMERIC(5,2) NOT NULL CHECK (accuracy_score BETWEEN 0 AND 100),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_assessments_session_id ON assessments(session_id);

-- ---------- feedback ----------
CREATE TABLE feedback (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    category        VARCHAR(30) NOT NULL
                        CHECK (category IN ('hand_shape', 'timing', 'position', 'motion')),
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
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
