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

    description: `Learn the ASL sign for ${letter}.`

  };

});
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
