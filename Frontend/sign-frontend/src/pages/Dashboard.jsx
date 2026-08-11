import { useEffect, useState } from "react";
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'
import BadgesStreaks from '../components/dashboard/BadgesStreaks.jsx'
import { getProgressReport } from "../services/api.js";
import { getUserId } from "../utils/auth.js";
import { recommendedSigns } from "../data/mockData.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = getUserId();
    if (!userId) {
      setLoading(false);
      return;
    }

    getProgressReport(userId)
      .then((data) =>
        setStats({
          accuracy: data.average_accuracy,
          lessonsCompleted: data.lessons_completed,
          practiceHours: (data.total_practice_time / 3600).toFixed(1),
        })
      )
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

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

          <div className="chart-grid">
            <AccuracyOverTimeChart />
            <LessonsCompletedChart />
          </div>
        </>
      )}

      <BadgesStreaks />

      {/* DEV ONLY: mock data, not wired to the recommendation API yet — see mockData.js */}
      <div className="recommend-box">
        <p className="recommend-box-title">
          <span className="hand-bullet" aria-hidden="true">🤟</span>
          Recommended Signs
          <span className="sparkle-dot gold" aria-hidden="true"></span>
        </p>
        <ul className="recommend-box-list">
          {recommendedSigns.map((rec) => (
            <li key={rec.id} className="recommend-chip">
              <span className="recommend-chip-sign">{rec.sign}</span>
              <span className="recommend-chip-reason">{rec.reason}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}