import { useState, useEffect } from 'react'
import { getUser } from '../utils/auth.js'
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'
import BadgesStreaks from '../components/dashboard/BadgesStreaks.jsx'

// DEV ONLY: mock stats/weekly-stats shaped exactly like the real
// /analytics/{id} and /weekly-analytics/{id} responses, so this can be
// swapped back to the live API calls later with no other changes needed.
const MOCK_STATS = {
  average_accuracy: 78,
  lessons_completed: 12,
  total_practice_time: 19800, // seconds -> 5.5h
}

const MOCK_WEEKLY_STATS = [
  { week_start: '2026-07-06', average_accuracy: 62, attempts_count: 3 },
  { week_start: '2026-07-13', average_accuracy: 68, attempts_count: 5 },
  { week_start: '2026-07-20', average_accuracy: 74, attempts_count: 4 },
  { week_start: '2026-07-27', average_accuracy: 81, attempts_count: 7 },
]

function formatWeekLabel(weekStartIso) {
  const d = new Date(weekStartIso)
  if (Number.isNaN(d.getTime())) return weekStartIso
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}

export default function Dashboard() {
  const user = getUser()

  const [stats, setStats] = useState(null)
  const [weeklyStats, setWeeklyStats] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate a quick load so the loading state still renders briefly,
    // matching the real (API-driven) version's behavior.
    const timer = setTimeout(() => {
      setStats(MOCK_STATS)
      setWeeklyStats(MOCK_WEEKLY_STATS)
      setIsLoading(false)
    }, 200)
    return () => clearTimeout(timer)
  }, [])

  if (!user) {
    return <p className="lessons-status error">You need to be logged in to view your dashboard.</p>
  }

  if (isLoading) {
    return <p className="lessons-status">Loading your dashboard...</p>
  }

  const accuracyData = weeklyStats.map((w) => ({
    day: formatWeekLabel(w.week_start),
    accuracy: Math.round(w.average_accuracy),
  }))

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

      <BadgesStreaks />
    </div>
  )
}