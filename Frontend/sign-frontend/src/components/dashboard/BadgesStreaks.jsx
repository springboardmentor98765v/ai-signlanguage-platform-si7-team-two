import { useEffect, useState } from "react";
import { getBadges, getStreak } from "../../services/api.js";
import { getUserId } from "../../utils/auth.js";

const ALL_BADGES = [
  { name: "Alphabet Master", description: "Completed every letter above 80% accuracy", icon: "🏆" },
  { name: "7-Day Streak", description: "Practiced 7 days in a row", icon: "🔥" },
  { name: "First Steps", description: "Completed your first lesson", icon: "👣" },
  { name: "Perfect Score", description: "Scored 100% accuracy on a letter", icon: "⭐" },
  { name: "30-Day Streak", description: "Practiced 30 days in a row", icon: "💎" },
  { name: "Speed Signer", description: "Completed 5 lessons in a single day", icon: "⚡" },
];

export default function BadgesStreaks() {
  const [earnedBadges, setEarnedBadges] = useState([]);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = getUserId();
    if (!userId) {
      setLoading(false);
      return;
    }

    Promise.all([getBadges(userId), getStreak(userId)])
      .then(([badgesData, streakData]) => {
        setEarnedBadges(badgesData);
        setStreak(streakData);
      })
      .catch((err) => console.error("Failed to load badges/streak:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  return (
    <section className="badges-section" aria-labelledby="badges-heading">
      <div className="badges-header">
        <h2 id="badges-heading">Badges &amp; Streaks</h2>
        <div className="streak-counter">
          <span className="streak-flame" aria-hidden="true">🔥</span>
          <span>
            <strong>{streak?.current_streak ?? 0}</strong> day streak
          </span>
        </div>
      </div>

      <ul className="badges-grid">
        {ALL_BADGES.map((badge) => {
          const earned = earnedBadges.find((b) => b.badge_name === badge.name);
          return (
            <li
              key={badge.name}
              className={`badge-card ${earned ? "unlocked" : "locked"}`}
              title={earned ? `Unlocked on ${earned.earned_at}` : "Locked"}
            >
              <span className="badge-icon" aria-hidden="true">{badge.icon}</span>
              <span className="badge-name">{badge.name}</span>
              <span className="badge-description">{badge.description}</span>
              {!earned && <span className="badge-locked-label">Locked</span>}
            </li>
          );
        })}
      </ul>
    </section>
  );
}