import { dashboardStats } from '../data/mockData.js'
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'

export default function Dashboard() {
  return (
    <div>
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
    </div>
  )
}
