-- Milestone 3 - Day 3
-- Performance indexes on fields that are searched often across the app.
-- (streaks.current_streak and notifications.user_id were already indexed on Day 2.)

-- 1. Login / auth lookups hit users.email on every request.
CREATE INDEX IF NOT EXISTS ix_users_email
    ON users (email);

-- 2. Lesson browse/search (Milestone 2 catalogue) filters by category constantly.
CREATE INDEX IF NOT EXISTS ix_lessons_category
    ON lessons (category);

-- 3. "Get this learner's badges" (Profile page, dashboard badge cards) is
--    a very frequent lookup filtered by learner_id.
CREATE INDEX IF NOT EXISTS ix_badges_learner_id
    ON badges (learner_id);
