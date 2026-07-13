import { reportSummary, attemptHistory, weakLetters } from '../data/mockData.js'

export default function Reports() {
  return (
    <div>
      <div className="reports-header">
        <h2>Your Progress Report</h2>
        <p className="sub">A summary of your accuracy, activity, and areas to improve.</p>
      </div>

      {/* Top summary stats — reuses the same stat-card style as Dashboard */}
      <div className="stats-grid">
        <div className="stat-card">
          <p className="label">Overall Accuracy</p>
          <p className="value">{reportSummary.overallAccuracy}%</p>
        </div>
        <div className="stat-card">
          <p className="label">Lessons Completed</p>
          <p className="value">{reportSummary.lessonsCompleted}</p>
        </div>
        <div className="stat-card">
          <p className="label">Practice Hours</p>
          <p className="value">{reportSummary.practiceHours}h</p>
        </div>
        <div className="stat-card">
          <p className="label">Improvement Rate</p>
          <p className="value">+{reportSummary.improvementRate}%</p>
        </div>
      </div>

      <div className="reports-grid">
        {/* Attempt history table */}
        <div className="report-panel">
          <p className="panel-title">Recent Attempts</p>
          <table className="attempts-table">
            <thead>
              <tr>
                <th>Letter</th>
                <th>Date</th>
                <th>Accuracy</th>
              </tr>
            </thead>
            <tbody>
              {attemptHistory.map((a) => (
                <tr key={a.id}>
                  <td className="letter-cell">{a.letter}</td>
                  <td>{a.date}</td>
                  <td>
                    <div className="accuracy-bar-wrap">
                      <div
                        className={`accuracy-bar ${a.accuracy < 70 ? 'low' : ''}`}
                        style={{ width: `${a.accuracy}%` }}
                      />
                      <span>{a.accuracy}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Weak letters / recommendations */}
        <div className="report-panel">
          <p className="panel-title">Recommended Practice</p>
          <div className="weak-letter-list">
            {weakLetters.map((w) => (
              <div className="weak-letter-item" key={w.letter}>
                <div className="weak-letter-badge">{w.letter}</div>
                <div className="weak-letter-info">
                  <p className="weak-letter-accuracy">{w.averageAccuracy}% avg accuracy</p>
                  <p className="weak-letter-hint">{w.sessionsRecommended} practice sessions recommended</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
