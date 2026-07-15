import { useState, useEffect } from "react";
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

  useEffect(() => {
    let isMounted = true;

    async function fetchLessons() {
      console.log("Fetching lessons...");
      setIsLoading(true);
      setError("");

      try {
        const data = await getLessons();

        if (isMounted) {
          setLessons(data);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || "Could not load lessons.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchLessons();

    return () => {
      isMounted = false;
    };
  }, []);

  if (isLoading) {
    return <p className="lessons-status">Loading lessons...</p>;
  }
if (error) {
  return (
    <p className="lessons-status error">
      {error}
    </p>
  )
}

  return <LessonGrid lessons={lessons} navigate={navigate} />;
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
