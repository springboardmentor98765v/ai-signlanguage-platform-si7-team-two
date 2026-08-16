import { useEffect, useState } from "react";
import BadgesStreaks from '../components/dashboard/BadgesStreaks.jsx'
import { getAnalyticsSummary, getRecommendations } from "../services/api.js";
import { getUserId } from "../utils/auth.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  function loadDashboard() {
    const userId = getUserId();
    if (!userId) {
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(false);

    Promise.all([
      getAnalyticsSummary(userId),
      // Weekly analytics 404s for a learner with zero sessions — that's
      // the empty state, not an error, so treat it as "no weeks yet".
      getRecommendations(userId).catch(() => ({ recommendations: [] })),
    ])
      .then(([progress, recs]) => {
        setStats({
          accuracy: progress.average_accuracy,
          lessonsCompleted: progress.lessons_completed,
          practiceHours: (progress.total_practice_time / 3600).toFixed(1),
        });
        setRecommendations(recs.recommendations || []);
      })
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) return null;

  if (error) {
    return (
      <div className="empty-page" role="alert">
        <h2>Couldn't load your dashboard</h2>
        <p>Something went wrong while fetching your stats. Please try again.</p>
        <button className="btn-primary" onClick={loadDashboard}>
          Try Again
        </button>
      </div>
    );
  }

  const hasActivity = stats && stats.lessonsCompleted > 0;

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
            <div className="stat-card fade-up">
              <p className="label">Accuracy</p>
              <p className="value">{stats.accuracy}%</p>
            </div>
            <div className="stat-card fade-up">
              <p className="label">Lessons Completed</p>
              <p className="value">{stats.lessonsCompleted}</p>
            </div>
            <div className="stat-card fade-up">
              <p className="label">Practice Hours</p>
              <p className="value">{stats.practiceHours}h</p>
            </div>
          </div>

        </>
      )}

      <BadgesStreaks />

      {recommendations.length > 0 && (
        <div className="recommend-box">
          <p className="recommend-box-title">
            <span className="hand-bullet" aria-hidden="true">🤟</span>
            Recommended Signs
            <span className="sparkle-dot gold" aria-hidden="true"></span>
          </p>
          <ul className="recommend-box-list">
            {recommendations.map((rec) => (
              <li key={rec.id} className="recommend-chip">
                <span className="recommend-chip-sign">{rec.letter_or_word}</span>
                <span className="recommend-chip-reason">{rec.reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
