import { dashboardStats } from '../data/mockData.js'
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'
import BadgesStreaks from '../components/dashboard/BadgesStreaks.jsx'

// Milestone 3, Day 7: empty state for a learner with no practice history yet.
// Real data will eventually come from the Reports/Progress API; for now this
// checks the mock stats the same way the real payload would (0 lessons
// completed = nothing to show yet).
const hasActivity = dashboardStats.lessonsCompleted > 0

export default function Dashboard() {
  return (
    <div>
      <h1 className="sr-only">Dashboard Overview</h1>

      {!hasActivity ? (
        <div className="empty-page" role="status">
          <h2>No activity yet</h2>
          <p>
            You haven't practiced any lessons yet — start with Letter A to
            see your stats here!
          </p>
        </div>
      ) : (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <p className="label">Accuracy</p>
              <p className="value">{dashboardStats.accuracy}%</p>
            </div>
            <div className="stat-card">
              <p className="label">Lessons Completed</p>
              <p className="value">{dashboardStats.lessonsCompleted}</p>
            </div>
            <div className="stat-card">
              <p className="label">Practice Hours</p>
              <p className="value">{dashboardStats.practiceHours}h</p>
            </div>
          </div>

          <div className="chart-grid">
            <AccuracyOverTimeChart />
            <LessonsCompletedChart />
          </div>
        </>
      )}

      <BadgesStreaks />
    </div>
  )
}