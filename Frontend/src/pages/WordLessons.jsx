import { useNavigate } from "react-router-dom";

const words = [
  "Bad",
  "Book",
  "Bus",
  "Busy",
  "Correct",
  "Father",
  "Fine",
  "Finish",
  "Forget",
  "Go",
  "Good",
  "Happy",
  "Hello",
  "Help",
  "More",
  "Mother",
  "No",
  "Not",
  "Please",
  "Sad",
  "School",
  "Thanks",
  "Wrong",
  "Yes"
];

export default function WordLessons() {
  const navigate = useNavigate();

  function openWord(word) {
    navigate(`/word-practice/${encodeURIComponent(word)}`);
  }

  return (
    <div>
      <h1 className="sr-only">Word Sign Lessons</h1>

      <div className="section-header">
        <h2 className="page-title">Word Sign Lessons</h2>
        <p className="page-sub">
          Select a word and practice its sign using your camera.
        </p>
      </div>

      <div className="lesson-grid">
        {words.map((word) => (
          <div
            key={word}
            className="lesson-card"
            onClick={() => openWord(word)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                openWord(word);
              }
            }}
          >
            <div className="lesson-card-header">
              <h3>{word}</h3>

              <span className="lesson-status-pill lesson-status--word">
                Word Sign
              </span>
            </div>

            <p>
              Practice the sign for <strong>{word}</strong> using
              real-time AI recognition.
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}