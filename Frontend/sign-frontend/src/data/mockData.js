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

// DEV ONLY (Milestone 3, Day 2): stands in for Intern 2's Notification API (due Day 4)
export const notifications = [
  {
    id: 1,
    type: 'badge',
    message: "You earned the 'Alphabet Master' badge!",
    createdAt: '2026-07-18T09:15:00',
    read: false,
  },
  {
    id: 2,
    type: 'recommendation',
    message: 'New recommendation available: practice letter M',
    createdAt: '2026-07-18T08:02:00',
    read: false,
  },
  {
    id: 3,
    type: 'streak',
    message: "You're on a 7-day streak! Keep it going.",
    createdAt: '2026-07-17T19:40:00',
    read: false,
  },
  {
    id: 4,
    type: 'certificate',
    message: 'Your certificate for Beginner Level is ready to download',
    createdAt: '2026-07-15T12:00:00',
    read: true,
  },
  {
    id: 5,
    type: 'system',
    message: 'Welcome to SignLearn! Start with Letter A to begin your journey.',
    createdAt: '2026-07-10T10:00:00',
    read: true,
  },
]

// DEV ONLY (Milestone 3, Day 3): stands in for Intern 4's Badge/Streak logic (due Day 3-4)
export const streakData = {
  currentStreak: 7,
  longestStreak: 12,
}

// DEV ONLY (Milestone 3, Day 4): stands in for Intern 4's Leaderboard ranking
// API (due Day 4) — see FR-4 / dependency matrix: Leaderboard ranking API ->
// Leaderboard page. `isCurrentUser` marks the logged-in learner (Aisha Khan,
// matches `currentUser` above) so their row can be highlighted.
export const leaderboardData = [
  { id: 1, name: 'Ananya Iyer', accuracy: 92, streak: 14, isCurrentUser: false },
  { id: 2, name: 'Meera Nair', accuracy: 88, streak: 9, isCurrentUser: false },
  { id: 3, name: 'Aisha Khan', accuracy: 84, streak: 7, isCurrentUser: true },
  { id: 4, name: 'Karan Shah', accuracy: 71, streak: 4, isCurrentUser: false },
  { id: 5, name: 'Rohan Verma', accuracy: 64, streak: 2, isCurrentUser: false },
  { id: 6, name: 'Divya Reddy', accuracy: 55, streak: 1, isCurrentUser: false },
]

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
