-- ============================================================
-- Draft seed data (Day 1 deliverable, NOT executed yet).
-- Real seeding is a Day 5 task (SRS §6, Intern 2 Day 5: "seed
-- sample data for the Alphabet course"), run once schema.sql
-- has been applied to a live DB (Day 2).
--
-- Included here now so Intern 2/4 can see the exact seed shape
-- while building their services, and so review of the schema
-- includes a sanity-check of realistic data.
-- ============================================================

INSERT INTO roles (name) VALUES
    ('Learner'), ('Instructor'), ('Trainer'), ('Admin')
ON CONFLICT (name) DO NOTHING;

-- Only the 5 sample letters Intern 3 targets for M1 (SRS §6, Intern 3 Day 4)
-- are seeded now; the remaining A-Z set is Intern 2's Day 5 full seed.
WITH new_course AS (
    INSERT INTO courses (name, level, description)
    VALUES ('Alphabet', 'Beginner', 'Learn the ASL alphabet, A-Z.')
    RETURNING id
)
INSERT INTO lessons (course_id, letter, title, order_index)
SELECT new_course.id, letter, 'Letter ' || letter, ord
FROM new_course,
     (VALUES ('A', 1), ('B', 2), ('C', 3), ('L', 4), ('Y', 5)) AS l(letter, ord);
