import { useState } from 'react'

// DEV ONLY (Milestone 3, Day 4): leaderboard data is mocked here.
// Real data will come from the Leaderboard ranking API later.
const MOCK_LEADERBOARD = [
  { id: 1, name: 'Meera Nair', accuracy: 88, streak: 12, isCurrentUser: false },
  { id: 2, name: 'Rohan Verma', accuracy: 64, streak: 4, isCurrentUser: false },
  { id: 3, name: 'Ananya Iyer', accuracy: 92, streak: 20, isCurrentUser: false },
  { id: 4, name: 'You', accuracy: 78, streak: 7, isCurrentUser: true },
  { id: 5, name: 'Divya Reddy', accuracy: 55, streak: 2, isCurrentUser: false },
]

const METRICS = {
  accuracy: { label: 'By Accuracy', unit: '%', key: 'accuracy' },
  streak: { label: 'By Streak', unit: ' days', key: 'streak' },
}

function medalFor(rank) {
  if (rank === 1) return '🥇'
  if (rank === 2) return '🥈'
  if (rank === 3) return '🥉'
  return null
}

export default function Leaderboard() {
  const [metric, setMetric] = useState('accuracy')
  const activeMetric = METRICS[metric]

  const ranked = [...MOCK_LEADERBOARD]
    .sort((a, b) => b[activeMetric.key] - a[activeMetric.key])
    .map((entry, index) => ({ ...entry, rank: index + 1 }))

  return (
    <div>
      <div className="reports-header">
        <h2>Leaderboard</h2>
        <p className="sub">
          See how you stack up against the rest of your class. This is just for fun and motivation!
        </p>
      </div>

      <div className="leaderboard-toggle" role="group" aria-label="Rank leaderboard by">
        {Object.entries(METRICS).map(([key, { label }]) => (
          <button
            key={key}
            type="button"
            className={`toggle-btn ${metric === key ? 'active' : ''}`}
            aria-pressed={metric === key}
            onClick={() => setMetric(key)}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="report-panel">
        <p className="panel-title" id="leaderboard-table-caption">
          Class ranking ({activeMetric.label.toLowerCase()})
        </p>

        <div
          className="table-scroll"
          role="region"
          aria-labelledby="leaderboard-table-caption"
          tabIndex={0}
        >
          <table className="attempts-table leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>{metric === 'accuracy' ? 'Accuracy' : 'Streak'}</th>
              </tr>
            </thead>
            <tbody>
              {ranked.map((entry) => (
                <tr
                  key={entry.id}
                  className={entry.isCurrentUser ? 'leaderboard-row current-user-row' : 'leaderboard-row'}
                >
                  <td>
                    <span className="rank-cell">
                      {medalFor(entry.rank) && <span aria-hidden="true">{medalFor(entry.rank)}</span>}
                      <span className={medalFor(entry.rank) ? 'sr-only' : ''}>#{entry.rank}</span>
                    </span>
                  </td>
                  <td>
                    {entry.name}
                    {entry.isCurrentUser && <span className="you-label">You</span>}
                  </td>
                  <td>
                    {entry[activeMetric.key]}
                    {activeMetric.unit}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}