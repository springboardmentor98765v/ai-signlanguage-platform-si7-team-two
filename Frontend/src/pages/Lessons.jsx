import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { getLessonsWithProgress } from "../services/api.js";
import { getUserId } from "../utils/auth.js";

function statusLabel(status) {
  if (status === "completed") return "Completed";
  if (status === "current") return "In progress";
  return "Locked";
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
      const userId = getUserId();
      const data = await getLessonsWithProgress(userId);
      setLessons(data);
    } catch (err) {
      setError(
        "We couldn't load your lessons right now. Please check your connection and try again."
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLessons();
  }, [fetchLessons]);

  function openLesson(letter) {
    navigate(`/practice/${letter}`);
  }

  function handleKeyDown(e, letter) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openLesson(letter);
    }
  }

  return (
    <div>
      <h1 className="sr-only">Lessons</h1>

      {isLoading ? (
        <div className="lessons-skeleton" role="status" aria-label="Loading lessons">
          <div className="lesson-skeleton" />
          <div className="lesson-skeleton" />
          <div className="lesson-skeleton" />
          <div className="lesson-skeleton" />
          <div className="lesson-skeleton" />
          <div className="lesson-skeleton" />
        </div>
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
          <div className="section-header">
            <h2 className="page-title">Your Lessons</h2>
            <p className="page-sub">Continue your sign language journey.</p>
          </div>

          <div className="lesson-grid">
            {lessons.map((lesson) => (
              <div
                key={lesson.id}
                className={`lesson-card lesson-card--${lesson.status}`}
                onClick={() => openLesson(lesson.letter)}
                onKeyDown={(e) => handleKeyDown(e, lesson.letter)}
                tabIndex={0}
                role="button"
                aria-label={`Open lesson: ${lesson.title}, status: ${lesson.status}`}
              >
                <div className="lesson-card-header">
                  <h3>{lesson.title}</h3>
                  <span className="lesson-status-pill">{statusLabel(lesson.status)}</span>
                </div>

                <p>{lesson.description}</p>

                <div className="lesson-card-footer">
                  <span className="lesson-meta">
                    {lesson.stars > 0 ? (
                      <span className="lesson-stars" aria-label={`${lesson.stars} stars`}>
                        {"⭐".repeat(lesson.stars)}
                      </span>
                    ) : (
                      <span className="lesson-meta-muted">Not started</span>
                    )}
                  </span>
                  <span className="lesson-accuracy">
                    {lesson.accuracy > 0 ? `${lesson.accuracy.toFixed(1)}%` : "—"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
