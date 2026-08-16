-- ============================================================
-- Milestone 1 — Database Schema
-- Dialect: PostgreSQL 14+
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- ROLES
-- ============================================================

CREATE TABLE roles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(30) NOT NULL UNIQUE
);

-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id         UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    full_name       VARCHAR(120) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_role_id ON users(role_id);

-- ============================================================
-- COURSES
-- ============================================================

CREATE TABLE courses (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(120) NOT NULL,
    level       VARCHAR(20) NOT NULL
                    CHECK (level IN ('Beginner', 'Intermediate', 'Advanced')),
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- LESSONS
-- ============================================================

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

-- ============================================================
-- PRACTICE SESSIONS
-- ============================================================

CREATE TABLE practice_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id       UUID NOT NULL REFERENCES lessons(id) ON DELETE RESTRICT,
    expected_sign   VARCHAR(2) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'in_progress'
                        CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    attempt_count   INT NOT NULL DEFAULT 0,

    -- Changed from start_time to started_at
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Changed from end_time to ended_at
    ended_at        TIMESTAMPTZ
);

CREATE INDEX idx_sessions_user_id ON practice_sessions(user_id);
CREATE INDEX idx_sessions_lesson_id ON practice_sessions(lesson_id);

-- ============================================================
-- ASSESSMENTS
-- ============================================================

CREATE TABLE assessments (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id              UUID NOT NULL REFERENCES practice_sessions(id) ON DELETE CASCADE,
    predicted_sign          VARCHAR(2) NOT NULL,
    confidence              NUMERIC(5,4) NOT NULL
                                CHECK (confidence BETWEEN 0 AND 1),
    hand_shape_score        NUMERIC(5,2) NOT NULL
                                CHECK (hand_shape_score BETWEEN 0 AND 100),
    finger_position_score   NUMERIC(5,2) NOT NULL
                                CHECK (finger_position_score BETWEEN 0 AND 100),
    timing_score            NUMERIC(5,2) NOT NULL
                                CHECK (timing_score BETWEEN 0 AND 100),
    motion_score            NUMERIC(5,2) NOT NULL
                                CHECK (motion_score BETWEEN 0 AND 100),
    position_score          NUMERIC(5,2) NOT NULL
                                CHECK (position_score BETWEEN 0 AND 100),
    overall_score           NUMERIC(5,2) NOT NULL
                                CHECK (overall_score BETWEEN 0 AND 100),
    is_correct              BOOLEAN NOT NULL,
    raw_landmarks           JSONB,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_assessments_session_id
ON assessments(session_id);

-- ============================================================
-- FEEDBACK
-- ============================================================

CREATE TABLE feedback (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id   UUID NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    category        VARCHAR(30) NOT NULL
                        CHECK (
                            category IN (
                                'hand_shape',
                                'finger_position',
                                'timing',
                                'position',
                                'motion'
                            )
                        ),
    severity        VARCHAR(20)
                        CHECK (
                            severity IN (
                                'minor',
                                'moderate',
                                'major'
                            )
                        ),
    message         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_feedback_assessment_id
ON feedback(assessment_id);

-- ============================================================
-- ANALYTICS SUMMARY
-- ============================================================

CREATE TABLE analytics_summary (
    user_id             UUID PRIMARY KEY
                            REFERENCES users(id) ON DELETE CASCADE,
    average_accuracy    NUMERIC(5,2) NOT NULL DEFAULT 0,
    lessons_completed   INT NOT NULL DEFAULT 0,
    total_practice_time INT NOT NULL DEFAULT 0,
    weak_letters        JSONB NOT NULL DEFAULT '[]',
    last_updated        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- CERTIFICATES
-- ============================================================

CREATE TABLE certificates (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL
                            REFERENCES users(id) ON DELETE CASCADE,
    average_score       REAL NOT NULL,
    lessons_completed   INT NOT NULL DEFAULT 0,
    certificate_code    VARCHAR(64) NOT NULL UNIQUE,
    file_path           VARCHAR(255),
    issued_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_valid             BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX idx_certificates_learner_id
ON certificates(learner_id);

CREATE INDEX idx_certificates_certificate_code
ON certificates(certificate_code);

-- ============================================================
-- RECOMMENDATIONS
-- ============================================================

CREATE TABLE recommendations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL
                            REFERENCES users(id) ON DELETE CASCADE,
    letter_or_word      VARCHAR(50) NOT NULL,
    reason              VARCHAR(255) NOT NULL,
    recent_avg_accuracy REAL,
    status              VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at         TIMESTAMPTZ
);

CREATE INDEX idx_recommendations_learner_id
ON recommendations(learner_id);

CREATE INDEX idx_recommendations_status
ON recommendations(status);

-- ============================================================
-- NOTIFICATIONS
-- ============================================================

CREATE TABLE notifications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL
                    REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(100) NOT NULL,
    message     VARCHAR(500) NOT NULL,
    is_read     BOOLEAN NOT NULL DEFAULT false,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_user_id
ON notifications(user_id);

-- ============================================================
-- STREAKS
-- ============================================================

CREATE TABLE streaks (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL UNIQUE
                            REFERENCES users(id) ON DELETE CASCADE,
    current_streak      INT NOT NULL DEFAULT 1,
    longest_streak      INT NOT NULL DEFAULT 1,
    last_practice_date  DATE
);

-- ============================================================
-- BADGES
-- ============================================================

CREATE TABLE badges (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id  UUID NOT NULL
                    REFERENCES users(id) ON DELETE CASCADE,
    badge_name  VARCHAR(100) NOT NULL,
    earned_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_badges_learner_id ON badges(learner_id);

-- ---------- accessibility_trainer_learner_mapping ----------
CREATE TABLE accessibility_trainer_learner_mapping (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trainer_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    learner_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (trainer_id, learner_id)
);

CREATE INDEX idx_mapping_trainer_id ON accessibility_trainer_learner_mapping(trainer_id);
CREATE INDEX idx_mapping_learner_id ON accessibility_trainer_learner_mapping(learner_id);

-- ---------- certification_exams ----------
CREATE TABLE certification_exams (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learner_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    level               VARCHAR(20) NOT NULL CHECK (level IN ('Beginner', 'Intermediate', 'Advanced', 'Professional')),
    score               NUMERIC(5,2) NOT NULL CHECK (score BETWEEN 0 AND 100),
    is_passed           BOOLEAN NOT NULL,
    taken_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    certificate_id      UUID REFERENCES certificates(id) ON DELETE SET NULL
);

CREATE INDEX idx_certification_exams_learner_id ON certification_exams(learner_id);
