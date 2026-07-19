// DEV ONLY: stands in for Intern 2's Instructor-Student API (due Day 6)
export const instructorStudents = [
  {
    id: 1,
    name: 'Meera Nair',
    accuracy: 88,
    lessonsCompleted: 14,
    lastActive: '2026-07-17',
    weakLetters: ['M', 'N'],
  },
  {
    id: 2,
    name: 'Rohan Verma',
    accuracy: 64,
    lessonsCompleted: 8,
    lastActive: '2026-07-16',
    weakLetters: ['R', 'S', 'V'],
  },
  {
    id: 3,
    name: 'Ananya Iyer',
    accuracy: 92,
    lessonsCompleted: 20,
    lastActive: '2026-07-18',
    weakLetters: [],
  },
  {
    id: 4,
    name: 'Karan Shah',
    accuracy: 71,
    lessonsCompleted: 11,
    lastActive: '2026-07-15',
    weakLetters: ['K', 'H'],
  },
  {
    id: 5,
    name: 'Divya Reddy',
    accuracy: 55,
    lessonsCompleted: 5,
    lastActive: '2026-07-12',
    weakLetters: ['D', 'Y', 'Q'],
  },
]

// DEV ONLY: stands in for Intern 2's Admin API (due Day 4)
export const adminUsers = [
  { id: 1, name: 'Aisha Khan', email: 'aisha.khan@example.com', role: 'Learner', active: true },
  { id: 2, name: 'Meera Nair', email: 'meera.nair@example.com', role: 'Learner', active: true },
  { id: 3, name: 'Rohan Verma', email: 'rohan.verma@example.com', role: 'Learner', active: true },
  { id: 4, name: 'Priya Menon', email: 'priya.menon@example.com', role: 'Instructor', active: true },
  { id: 5, name: 'Divya Reddy', email: 'divya.reddy@example.com', role: 'Learner', active: false },
  { id: 6, name: 'Sameer Gupta', email: 'sameer.gupta@example.com', role: 'Instructor', active: true },
]

export const dashboardStats = {
  accuracy: 78,
  lessonsCompleted: 12,
  practiceHours: 5.5,
};

export const lessons = Array.from({ length: 26 }, (_, index) => {

  const letter = String.fromCharCode(65 + index);

  return {

    id: index + 1,

    title: `Letter ${letter}`,

    letter,

    difficulty:
      index < 9
        ? "Beginner"
        : index < 18
        ? "Intermediate"
        : "Advanced",

    description: `Learn the ASL sign for ${letter}.`,

    learnersUsing: 8 + ((index * 3) % 40),

  };

});
// DEV ONLY: stands in for Intern 2's Profile API (due later) — used for certificate name
export const currentUser = {
  name: 'Aisha Khan',
  email: 'aisha.khan@example.com',
  role: 'Learner',
}

export const reportSummary = {
  overallAccuracy: 87,
  lessonsCompleted: 12,
  practiceHours: 24,
  improvementRate: 12,
}

export const attemptHistory = [
  { id: 1, letter: 'A', date: '2026-07-08', accuracy: 92 },
  { id: 2, letter: 'B', date: '2026-07-08', accuracy: 81 },
  { id: 3, letter: 'C', date: '2026-07-09', accuracy: 75 },
  { id: 4, letter: 'M', date: '2026-07-10', accuracy: 58 },
  { id: 5, letter: 'N', date: '2026-07-10', accuracy: 63 },
  { id: 6, letter: 'A', date: '2026-07-11', accuracy: 95 },
]

export const weakLetters = [
  { letter: 'M', averageAccuracy: 58, sessionsRecommended: 5 },
  { letter: 'N', averageAccuracy: 63, sessionsRecommended: 4 },
  { letter: 'R', averageAccuracy: 66, sessionsRecommended: 3 },
]
