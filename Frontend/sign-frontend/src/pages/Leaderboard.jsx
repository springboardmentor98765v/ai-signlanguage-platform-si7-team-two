import { useState, useEffect, useCallback } from 'react'
import { getLeaderboard } from '../services/api.js'
import { getUser } from '../utils/auth.js'
import ChampionsRise from '../components/leaderboard/ChampionsRise.jsx'
import Mascot from '../components/mascot/Mascot.jsx'
import { MASCOTS, getActiveMascotId } from '../components/mascot/MascotPicker.jsx'

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

/** Determine mascot state based on the current user's rank in the list. */
function mascotStateFor(entries, currentUser) {
  if (!currentUser) return 'encouraging'
  const mine = entries.find(
    (e) => e.learner_id === currentUser.id || e.learner_id === String(currentUser.id)
  )
  if (!mine) return 'encouraging'
  if (mine.rank === 1) return 'celebrating'
  if (mine.rank <= 5) return 'encouraging'
  return 'idle'
}

/** Bubble text based on mascot state and user rank. */
function mascotLabel(entries, currentUser) {
  if (!currentUser) return 'You can do it! 💪'
  const mine = entries.find(
    (e) => e.learner_id === currentUser.id || e.learner_id === String(currentUser.id)
  )
  if (!mine) return 'Keep practising! 🌟'
  if (mine.rank === 1) return "You're #1! 🏆"
  if (mine.rank <= 3) return `#${mine.rank} — great work!`
  if (mine.rank <= 5) return `#${mine.rank} — almost there!`
  return `#${mine.rank} — keep going!`
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

  const mState = entries.length > 0 ? mascotStateFor(entries, currentUser) : 'idle'
  const mLabel = entries.length > 0 ? mascotLabel(entries, currentUser) : undefined

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
          {/* Mascot reacting to the current user's position */}
          <div className="leaderboard-mascot-row" aria-hidden="true">
            <Mascot state={mState} size="md" label={mLabel} mascotId={currentUser?.mascot_id} aria-hidden={true} />
          </div>

          <ChampionsRise entries={entries} unit={activeMetric.unit} currentUser={currentUser} />

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
                    currentUser &&
                    (entry.learner_id === currentUser.id || entry.learner_id === String(currentUser.id))
                  const isFirst = entry.rank === 1
                  return (
                    <tr
                      key={entry.learner_id}
                      className={[
                        'leaderboard-row',
                        isCurrentUser ? 'current-user-row' : '',
                        isFirst ? 'rank-1-row' : '',
                      ].filter(Boolean).join(' ')}
                    >
                      <td>
                        <span className="rank-cell">
                          {isFirst ? (
                            <span className="rank-dance-icon" aria-hidden="true">🥇</span>
                          ) : medalFor(entry.rank) ? (
                            <span aria-hidden="true">{medalFor(entry.rank)}</span>
                          ) : null}
                          <span className={medalFor(entry.rank) ? 'sr-only' : ''}>
                            #{entry.rank}
                          </span>
                        </span>
                      </td>
                      <td className="leaderboard-name-cell">
                        {(() => {
                          let effectiveMascotId = entry.mascot_id
                          if (isCurrentUser) {
                            effectiveMascotId = currentUser.mascot_id || getActiveMascotId()
                          }
                          const mascotDef = MASCOTS.find((m) => m.id === effectiveMascotId)
                          return (
                            <div className="list-avatar" style={{ '--avatar-bg': mascotDef?.color }}>
                              {mascotDef ? (
                                <span aria-hidden="true">{mascotDef.emoji}</span>
                              ) : (
                                entry.learner_name.charAt(0).toUpperCase()
                              )}
                            </div>
                          )
                        })()}
                        {entry.learner_name}
                        {isCurrentUser && <span className="you-label">You</span>}
                        {isFirst && <span className="rank-1-crown" aria-hidden="true"> 👑</span>}
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