import { useState, useEffect } from 'react'
import { getUser } from '../utils/auth.js'
import { getLearnerAnalytics, getWeeklyAnalytics } from '../services/api.js'
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'

function formatWeekLabel(weekStartIso) {
  const d = new Date(weekStartIso)
  if (Number.isNaN(d.getTime())) return weekStartIso
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}

export default function Dashboard() {
  const user = getUser()

  const [stats, setStats] = useState(null)
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!user) {
      setIsLoading(false)
      return
    }

    let isMounted = true

    async function loadDashboard() {
      setIsLoading(true)
      setError('')
      try {
        const [analytics, weekly] = await Promise.all([
          getLearnerAnalytics(user.id),
          getWeeklyAnalytics(user.id),
        ])
        if (isMounted) {
          setStats(analytics)
          setWeeklyStats(weekly.weekly_stats || [])
        }
      } catch (err) {
        if (isMounted) {
          // Both /analytics/{id} and /weekly-analytics/{id} 404 until the learner has
          // at least one practice session recorded — this is the expected first-run state,
          // not a broken integration, so we show a friendly empty state instead of a scary error.
          setError(err.message || 'Could not load your dashboard yet.')
        }
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    loadDashboard()
    return () => { isMounted = false }
    // NOTE: depend on user?.id, not the whole user object. getUser() re-parses
    // localStorage on every render and returns a brand-new object each time, so
    // using [user] here made this effect re-fire on every single render forever
    // (infinite fetch loop). user?.id is a stable primitive, so this now only
    // re-runs when the actual logged-in user changes.
  }, [user?.id])

  if (!user) {
    return <p className="lessons-status error">You need to be logged in to view your dashboard.</p>
  }

  if (isLoading) {
    return <p className="lessons-status">Loading your dashboard...</p>
  }

  if (error || !stats) {
    return (
      <div>
        <p className="lessons-status">
          No practice history yet. Head to Practice and try a letter to start building your stats.
        </p>
      </div>
    )
  }

  const accuracyData = weeklyStats.map((w) => ({
    day: formatWeekLabel(w.week_start),
    accuracy: Math.round(w.average_accuracy),
  }))

  // The Business Logic service's weekly stats give attempts_count, not a
  // lessons-completed-per-week figure — labeling this "lessons completed" would
  // misrepresent the data, so the chart is honestly relabeled to what it is.
  const attemptsData = weeklyStats.map((w) => ({
    week: formatWeekLabel(w.week_start),
    attempts: w.attempts_count,
  }))

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-card">
          <p className="label">Accuracy</p>
          <p className="value">{Math.round(stats.average_accuracy)}%</p>
        </div>
        <div className="stat-card">
          <p className="label">Lessons Completed</p>
          <p className="value">{stats.lessons_completed}</p>
        </div>
        <div className="stat-card">
          <p className="label">Practice Hours</p>
          <p className="value">{(stats.total_practice_time / 3600).toFixed(1)}h</p>
        </div>
      </div>

      <div className="chart-grid">
        <AccuracyOverTimeChart
          data={accuracyData.length ? accuracyData : undefined}
          subtitle="Your weekly average accuracy."
        />
        <LessonsCompletedChart
          data={attemptsData.length ? attemptsData : undefined}
          title="Practice attempts"
          subtitle="Number of attempts you made each week."
          dataKey="attempts"
          valueLabel="Attempts"
        />
      </div>
    </div>
  )
}