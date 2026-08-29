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
      <div className="practice-header">
        <div>
          <h2>Word Sign Lessons</h2>

          <p className="sub">
            Select a word and practice its sign using your camera.
          </p>
        </div>
      </div>

      <div className="lesson-grid">
        {words.map((word) => (
          <div
            key={word}
            className="lesson-card"
            style={{ cursor: "pointer" }}
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

              <span className="badge badge-intermediate">
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