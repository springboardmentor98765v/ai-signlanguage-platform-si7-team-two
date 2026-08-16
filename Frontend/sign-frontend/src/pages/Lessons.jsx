import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { getLessons } from "../services/api.js";
import { getUser } from "../utils/auth.js";
import Mascot from "../components/mascot/Mascot.jsx";


function badgeClass(difficulty) {
  if (difficulty === "Beginner") return "badge badge-beginner";
  if (difficulty === "Intermediate") return "badge badge-intermediate";
  return "badge badge-advanced";
}

export default function Lessons() {
  const navigate = useNavigate();

  const [lessons, setLessons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchLessons = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        navigate("/login");
        return;
      }
      const data = await getLessons(userId);
      setLessons(data);
    } catch (err) {
      setError(
        "We couldn't load your lessons right now. Please check your connection and try again."
      );
    } finally {
      setIsLoading(false);
    }
  }, [navigate]);

  useEffect(() => {
    fetchLessons();
  }, [fetchLessons]);

  return (
    <div>
      <h1 className="sr-only">Lessons</h1>

      {isLoading ? (
        <p className="lessons-status" role="status">
          Loading lessons...
        </p>
      ) : error ? (
        <div className="empty-page" role="alert">
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <button className="btn-secondary btn-inline" onClick={fetchLessons}>
            Try Again
          </button>
        </div>
      ) : lessons.length === 0 ? (
        <div className="empty-page" role="status">
          <h2>No lessons available yet</h2>
          <p>Check back soon — new lessons are added regularly!</p>
        </div>
      ) : (
        <>
          <h2 className="sr-only">Available Lessons</h2>
          <div className="lessons-mascot-row" aria-hidden="true">
            <Mascot state="encouraging" size="sm" label="Pick a lesson! 🖊️" mascotId={getUser()?.mascot_id} aria-hidden={true} />
          </div>
          <LessonGrid lessons={lessons} navigate={navigate} />
        </>
      )}
    </div>
  );
}

function LessonGrid({ lessons, navigate }) {
  function openLesson(lessonId, letter) {
    navigate(`/practice/${letter}?lessonId=${lessonId}`);
  }

  function handleKeyDown(e, lesson) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openLesson(lesson.id, lesson.letter);
    }
  }

  return (
    <div className="lesson-path">
      {lessons.map((lesson, index) => {
        const status = lesson.status || "locked";
        const starSymbols = "★".repeat(lesson.stars || 0) + "☆".repeat(3 - (lesson.stars || 0));
        
        return (
          <div
            key={lesson.id}
            className={`lesson-node status-${status} path-pos-${index % 4}`}
            onClick={() => status !== 'locked' && openLesson(lesson.id, lesson.letter)}
            onKeyDown={(e) => status !== 'locked' && handleKeyDown(e, lesson)}
            tabIndex={status !== 'locked' ? 0 : -1}
            role="button"
            aria-disabled={status === 'locked'}
            aria-label={`${lesson.title} - ${status}`}
          >
            <div className="node-icon">
              {status === 'completed' && <div className="stars-indicator">{starSymbols}</div>}
              {status === 'current' && '▶'}
              {status === 'locked' && '🔒'}
            </div>
            <div className="node-label">Letter {lesson.letter}</div>
            <div className="node-tooltip">
              <h3>{lesson.title}</h3>
              <p>{lesson.description}</p>
              {status === 'completed' && <p>Best: {lesson.accuracy}%</p>}
            </div>
          </div>
        )
      })}
    </div>
  );
}