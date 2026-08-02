import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { getLessons } from "../services/api.js";


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
      const data = await getLessons();
      setLessons(data);
    } catch (err) {
      // Milestone 3, Day 7: friendly, non-technical error message instead
      // of raw fetch/network error text.
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
          <LessonGrid lessons={lessons} navigate={navigate} />
        </>
      )}
    </div>
  );
}

function LessonGrid({ lessons, navigate }) {
  return (
    <div className="lesson-grid">
      {lessons.map((lesson) => (
        <div
          key={lesson.id}
          className="lesson-card"
          style={{ cursor: "pointer" }}
          onClick={() => navigate(`/practice/${lesson.letter}`)}
        >
          <div className="lesson-card-header">
            <h3>{lesson.title}</h3>

            <span className={badgeClass(lesson.difficulty)}>
              {lesson.difficulty}
            </span>
          </div>

          <p>{lesson.description}</p>
        </div>
      ))}
    </div>
  );
}