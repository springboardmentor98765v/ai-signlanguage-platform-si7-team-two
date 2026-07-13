export const dashboardStats = {
  accuracy: 78,
  lessonsCompleted: 12,
  practiceHours: 5.5,
};

export const lessons = [
  { id: 1, title: 'Alphabet A - E', difficulty: 'Beginner', description: 'Learn the first five letters of the sign alphabet.' },
  { id: 2, title: 'Alphabet F - J', difficulty: 'Beginner', description: 'Continue building your alphabet foundation.' },
  { id: 3, title: 'Alphabet K - O', difficulty: 'Intermediate', description: 'Practice mid-alphabet hand shapes.' },
  { id: 4, title: 'Alphabet P - T', difficulty: 'Intermediate', description: 'Refine finger positioning and timing.' },
  { id: 5, title: 'Alphabet U - Z', difficulty: 'Advanced', description: 'Master the final letters with speed drills.' },
  { id: 6, title: 'Common Greetings', difficulty: 'Beginner', description: 'Hello, thank you, please, and more.' },
]

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
