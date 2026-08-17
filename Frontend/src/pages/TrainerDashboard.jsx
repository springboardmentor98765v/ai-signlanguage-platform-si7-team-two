import { useEffect, useState } from "react";
import { getTrainerLearners, getTrainerAnalytics } from "../services/api";
import { getUser } from "../utils/auth";

export default function TrainerDashboard() {
  const [learners, setLearners] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  const user = getUser();
  const trainerId = user?.id;

  useEffect(() => {
    if (!trainerId) return;
    loadDashboardData();
  }, [trainerId]);

  async function loadDashboardData() {
    setLoading(true);
    try {
      const [learnersData, analyticsData] = await Promise.all([
        getTrainerLearners(trainerId),
        getTrainerAnalytics(trainerId)
      ]);
      setLearners(learnersData);
      setAnalytics(analyticsData);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard data. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  return (
    <div>
      <div className="reports-header">
        <h2>Accessibility Trainer Dashboard</h2>
        <p className="sub">Overview of your assigned learners and their progress.</p>
      </div>

      {error ? (
        <div className="empty-page" role="alert">
          <p>{error}</p>
          <button type="button" className="btn-secondary btn-inline" onClick={loadDashboardData}>
            Try Again
          </button>
        </div>
      ) : (
        <div className="reports-grid">
          {/* ANALYTICS PANEL */}
          <div className="report-panel">
            <p className="panel-title">Overall Analytics</p>
            {analytics ? (
              <>
                <div className="summary-row">
                  <span>Total Assigned Learners</span>
                  <span>{analytics.total_learners}</span>
                </div>
                <div className="summary-row">
                  <span>Average Score</span>
                  <span>{analytics.average_score}%</span>
                </div>
                <div className="summary-row">
                  <span>Total Practice Hours</span>
                  <span>{analytics.total_practice_hours} hrs</span>
                </div>
              </>
            ) : (
              <p className="lessons-status">No analytics available.</p>
            )}
          </div>

          {/* LEARNERS PANEL */}
          <div className="report-panel">
            <p className="panel-title">Assigned Learners ({learners.length})</p>
            {learners.length === 0 ? (
              <p className="lessons-status">No learners assigned yet.</p>
            ) : (
              <div className="table-scroll">
                <table className="attempts-table">
                  <thead>
                    <tr>
                      <th>Learner ID</th>
                      <th>Mapped Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {learners.map((mapping) => (
                      <tr key={mapping.id}>
                        <td>{mapping.learner_id}</td>
                        <td>{new Date(mapping.created_at).toLocaleDateString()}</td>
                        <td>{mapping.status || "active"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
