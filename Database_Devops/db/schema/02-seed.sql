-- ============================================================
-- Seed Roles
-- ============================================================

INSERT INTO roles (name)
VALUES
('Learner'),
('Instructor'),
('Trainer'),
('Admin')
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- Seed Alphabet Course
-- ============================================================

WITH new_course AS
(
    INSERT INTO courses
    (
        name,
        level,
        description
    )
    VALUES
    (
        'Alphabet',
        'Beginner',
        'Learn the complete ASL Alphabet (A-Z).'
    )
    ON CONFLICT DO NOTHING
    RETURNING id
)

INSERT INTO lessons
(
    course_id,
    letter,
    title,
    description,
    order_index
)

SELECT

new_course.id,

lesson,

'Letter ' || lesson,

'Practice the ASL sign for letter ' || lesson,

idx

FROM new_course,

(
VALUES
('A',1),
('B',2),
('C',3),
('D',4),
('E',5),
('F',6),
('G',7),
('H',8),
('I',9),
('J',10),
('K',11),
('L',12),
('M',13),
('N',14),
('O',15),
('P',16),
('Q',17),
('R',18),
('S',19),
('T',20),
('U',21),
('V',22),
('W',23),
('X',24),
('Y',25),
('Z',26)

) AS letters(lesson,idx);