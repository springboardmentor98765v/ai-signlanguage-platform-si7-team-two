import { useEffect, useState } from "react";
import AccuracyOverTimeChart from '../components/charts/AccuracyOverTimeChart.jsx'
import LessonsCompletedChart from '../components/charts/LessonsCompletedChart.jsx'
import BadgesStreaks from '../components/dashboard/BadgesStreaks.jsx'
import Mascot from '../components/mascot/Mascot.jsx'
import { getProgressReport, getWeeklyAnalytics } from "../services/api.js";
import { getUser, getUserId } from "../utils/auth.js";
import { recommendedSigns } from "../data/mockData.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [weeklyStats, setWeeklyStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = getUserId();
    if (!userId) {
      setLoading(false);
      return;
    }

    Promise.all([
      getProgressReport(userId),
      getWeeklyAnalytics(userId).catch(() => ({ weekly_stats: [] }))
    ])
      .then(([reportData, weeklyData]) => {
        setStats({
          accuracy: reportData.average_accuracy,
          lessonsCompleted: reportData.lessons_completed,
          practiceHours: (reportData.total_practice_time / 3600).toFixed(1),
        });
        setWeeklyStats(weeklyData.weekly_stats || []);
      })
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  const accuracyChartData = weeklyStats.map((stat) => ({
    day: stat.week_start,
    accuracy: Math.round(stat.average_accuracy),
  }));

  const lessonsChartData = weeklyStats.map((stat) => ({
    week: stat.week_start,
    lessons: stat.attempts_count,
  }));

  const hasActivity = stats && stats.lessonsCompleted > 0;
  // Mascot celebrates if accuracy is high, encourages otherwise
  const dashMascotState = hasActivity
    ? (stats.accuracy >= 80 ? 'celebrating' : 'encouraging')
    : 'idle'

  return (
    <div>
      <h1 className="sr-only">Dashboard Overview</h1>

      <div className="dashboard-mascot-row" aria-hidden="true">
        <Mascot
          state={dashMascotState}
          size="sm"
          mascotId={getUser()?.mascot_id}
          label={hasActivity
            ? (stats.accuracy >= 80 ? 'Great work! 🌟' : 'Keep going! 💪')
            : 'Let\'s start! 🤟'
          }
          aria-hidden={true}
        />
      </div>

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
            {accuracyChartData.length > 0 && (
              <AccuracyOverTimeChart data={accuracyChartData} />
            )}
            {lessonsChartData.length > 0 && (
              <LessonsCompletedChart data={lessonsChartData} />
            )}
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