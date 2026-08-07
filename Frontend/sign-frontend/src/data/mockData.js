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

// TEMP (Day 7 empty-state test): changed to all-zero to trigger Dashboard's
// empty state. Revert to accuracy: 78, lessonsCompleted: 12, practiceHours: 5.5
// once you've confirmed the empty state renders correctly.
export const dashboardStats = {
  accuracy: 0,
  lessonsCompleted: 0,
  practiceHours: 0,
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

export const notifications = [
  {
    id: 1,
    user_id: 1,
    title: 'New Badge Unlocked',
    message: 'You earned the "7-Day Streak" badge. Keep it up!',
    is_read: false,
    created_at: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
  },
  {
    id: 2,
    user_id: 1,
    title: 'Lesson Reminder',
    message: 'You have not practiced letter "M" in 3 days. Try a quick session.',
    is_read: false,
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 3,
    user_id: 1,
    title: 'Assessment Ready',
    message: 'Your weekly assessment results are ready to view.',
    is_read: false,
    created_at: new Date(Date.now() - 26 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 4,
    user_id: 1,
    title: 'Leaderboard Update',
    message: 'You moved up to #3 on the weekly leaderboard.',
    is_read: true,
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 5,
    user_id: 1,
    title: 'Certificate Available',
    message: 'Your "Alphabet Master" certificate is ready to download.',
    is_read: true,
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
  },
]

// DEV ONLY (Milestone 3, Day 3): stands in for Intern 4's Badge/Streak logic (due Day 3-4)
export const streakData = {
  currentStreak: 7,
  longestStreak: 12,
}

// TEMP (Day 7 empty-state test): changed to an empty array to trigger the
// Leaderboard's empty state. Revert to the full list of 6 entries once
// you've confirmed "No leaderboard data yet" renders correctly.
export const leaderboardData = []

export const badges = [
  {
    id: 1,
    name: 'Alphabet Master',
    description: 'Completed every letter above 80% accuracy',
    icon: '🏆',
    unlocked: true,
    unlockedOn: '2026-07-18',
  },
  {
    id: 2,
    name: '7-Day Streak',
    description: 'Practiced 7 days in a row',
    icon: '🔥',
    unlocked: true,
    unlockedOn: '2026-07-17',
  },
  {
    id: 3,
    name: 'First Steps',
    description: 'Completed your first lesson',
    icon: '👣',
    unlocked: true,
    unlockedOn: '2026-07-08',
  },
  {
    id: 4,
    name: 'Perfect Score',
    description: 'Scored 100% accuracy on a letter',
    icon: '⭐',
    unlocked: false,
  },
  {
    id: 5,
    name: '30-Day Streak',
    description: 'Practiced 30 days in a row',
    icon: '💎',
    unlocked: false,
  },
  {
    id: 6,
    name: 'Speed Signer',
    description: 'Completed 5 lessons in a single day',
    icon: '⚡',
    unlocked: false,
  },
]