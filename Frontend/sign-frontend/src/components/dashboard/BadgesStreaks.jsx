import { badges, streakData } from '../../data/mockData.js'

// DEV ONLY (Milestone 3, Day 3): badges/streak data is read from local mock
// data. Real data will come from Intern 4's Badge/Streak logic (due Day 3-4)
// — see FR-4 / dependency matrix: Badges/Streaks tables -> Badge/Streak
// logic -> this component.

export default function BadgesStreaks() {
  return (
    <section className="badges-section" aria-labelledby="badges-heading">
      <div className="badges-header">
        <h2 id="badges-heading">Badges &amp; Streaks</h2>
        <div className="streak-counter">
          <span className="streak-flame" aria-hidden="true">🔥</span>
          <span>
            <strong>{streakData.currentStreak}</strong> day streak
          </span>
        </div>
      </div>

      <ul className="badges-grid">
        {badges.map((badge) => (
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
