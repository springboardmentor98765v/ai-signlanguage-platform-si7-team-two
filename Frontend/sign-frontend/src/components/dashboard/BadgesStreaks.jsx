// DEV ONLY (Milestone 3, Day 3): badges/streak data is mocked here.
// Real data will come from Intern 4's Badge/Streak logic later.

const MOCK_STREAK = { currentStreak: 7 }

const MOCK_BADGES = [
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
    unlockedOn: '2026-07-08',
  },
  {
    id: 3,
    name: 'First Steps',
    description: 'Completed your first lesson',
    icon: '👣',
    unlocked: true,
    unlockedOn: '2026-06-30',
  },
  {
    id: 4,
    name: 'Perfect Score',
    description: 'Scored 100% accuracy on a letter',
    icon: '💎',
    unlocked: false,
  },
  {
    id: 5,
    name: '30-Day Streak',
    description: 'Practiced 30 days in a row',
    icon: '⚡',
    unlocked: false,
  },
]

export default function BadgesStreaks() {
  return (
    <section className="badges-section" aria-labelledby="badges-heading">
      <div className="badges-header">
        <h2 id="badges-heading">Badges &amp; Streaks</h2>
        <div className="streak-counter">
          <span className="streak-flame" aria-hidden="true">🔥</span>
          <span>
            <strong>{MOCK_STREAK.currentStreak}</strong> day streak
          </span>
        </div>
      </div>

      <ul className="badges-grid">
        {MOCK_BADGES.map((badge) => (
          <li
            key={badge.id}
            className={`badge-card ${badge.unlocked ? 'unlocked' : 'locked'}`}
            title={badge.unlocked ? `Unlocked on ${badge.unlockedOn}` : 'Locked'}
          >
            <span className="badge-icon" aria-hidden="true">
              {badge.icon}
            </span>
            <span className="badge-name">{badge.name}</span>
            <span className="badge-description">{badge.description}</span>
            {!badge.unlocked && <span className="badge-locked-label">Locked</span>}
          </li>
        ))}
      </ul>
    </section>
  )
}