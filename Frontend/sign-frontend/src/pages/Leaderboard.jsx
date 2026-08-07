import { useState, useEffect, useCallback } from 'react'
import { getLeaderboard } from '../services/api.js'
import { getUser } from '../utils/auth.js'
import ChampionsRise from '../components/leaderboard/ChampionsRise.jsx'

const METRICS = {
  accuracy: { label: 'By Accuracy', unit: '%', apiKey: 'accuracy' },
  streak: { label: 'By Streak', unit: ' days', apiKey: 'streak' },
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
  const currentUser = getUser()

  const [entries, setEntries] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchLeaderboard = useCallback(async () => {
    setIsLoading(true)
    setError('')
    try {
      const data = await getLeaderboard(activeMetric.apiKey)
      setEntries(data)
    } catch (err) {
      setError(
        "We couldn't load the leaderboard right now. Please check your connection and try again."
      )
    } finally {
      setIsLoading(false)
    }
  }, [activeMetric.apiKey])

  useEffect(() => {
    fetchLeaderboard()
  }, [fetchLeaderboard])

  return (
    <div>
      <h1 className="sr-only">Leaderboard</h1>
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

      {isLoading ? (
        <p className="lessons-status" role="status">Loading leaderboard...</p>
      ) : error ? (
        <div className="empty-page" role="alert">
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <button className="btn-secondary btn-inline" onClick={fetchLeaderboard}>
            Try Again
          </button>
        </div>
      ) : entries.length === 0 ? (
        <div className="empty-page" role="status">
          <h2>No leaderboard data yet</h2>
          <p>Start practicing to appear on the board!</p>
        </div>
      ) : (
        <div className="report-panel">
          <ChampionsRise entries={entries} unit={activeMetric.unit} />

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
                {entries.map((entry) => {
                  const isCurrentUser =
                    currentUser && entry.learner_id === currentUser.id
                  return (
                    <tr
                      key={entry.learner_id}
                      className={isCurrentUser ? 'leaderboard-row current-user-row' : 'leaderboard-row'}
                    >
                      <td>
                        <span className="rank-cell">
                          {medalFor(entry.rank) && (
                            <span aria-hidden="true">{medalFor(entry.rank)}</span>
                          )}
                          <span className={medalFor(entry.rank) ? 'sr-only' : ''}>
                            #{entry.rank}
                          </span>
                        </span>
                      </td>
                      <td>
                        {entry.learner_name}
                        {isCurrentUser && <span className="you-label">You</span>}
                      </td>
                      <td>
                        {Math.round(entry.score)}
                        {activeMetric.unit}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}