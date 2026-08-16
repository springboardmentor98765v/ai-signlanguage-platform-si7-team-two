import { useState } from "react";

// Milestone 4, Day 2-3 (SRS FR-4 / Section 9): Certification Exam workflow.
// A structured exam covering multiple signs at once (not one letter like
// regular Practice), with 4 pass/fail levels. Running on mock data today —
// real exam-scoring logic (Intern 4) and certificate trigger wire in once
// the backend endpoint exists.

const LEVELS = [
  {
    id: "beginner",
    name: "Beginner",
    description: "Covers the first 10 letters of the alphabet.",
    passThreshold: 70,
    signCount: 10,
  },
  {
    id: "intermediate",
    name: "Intermediate",
    description: "Covers all 26 letters of the alphabet.",
    passThreshold: 75,
    signCount: 26,
  },
  {
    id: "advanced",
    name: "Advanced",
    description: "Full alphabet plus common word signs.",
    passThreshold: 80,
    signCount: 30,
  },
  {
    id: "professional",
    name: "Professional",
    description: "Full alphabet, word signs, and timed recognition.",
    passThreshold: 90,
    signCount: 35,
  },
];

// Mock exam history — replace with a real
// GET /certification/history/{user_id} call once it exists.
const mockHistory = [
  {
    id: "mock-attempt-1",
    level: "Beginner",
    score: 82,
    passed: true,
    date: "2026-07-12",
  },
];

export default function Certification() {
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [examState, setExamState] = useState("idle"); // idle | in-progress | result
  const [mockResult, setMockResult] = useState(null);

  function startExam(level) {
    setSelectedLevel(level);
    setExamState("in-progress");
  }

  function finishMockExam() {
    // Placeholder scoring until the real exam-scoring endpoint exists.
    // Intentionally random-ish so the UI's pass/fail branches are both
    // visible during testing, not a real assessment.
    const score = Math.floor(Math.random() * 31) + 65; // 65-95
    const passed = score >= selectedLevel.passThreshold;
    setMockResult({ score, passed });
    setExamState("result");
  }

  function resetExam() {
    setSelectedLevel(null);
    setExamState("idle");
    setMockResult(null);
  }

  return (
    <div>
      <h1 className="sr-only">Certification Exam</h1>
      <div className="reports-header">
        <h2>Certification Exam</h2>
        <p className="sub">
          Take a structured exam to earn an official certificate for your
          sign language level.
        </p>
      </div>

      {examState === "idle" && (
        <>
          <div className="lesson-grid">
            {LEVELS.map((level) => (
              <div key={level.id} className="lesson-card fade-up">
                <div className="lesson-card-header">
                  <h3>{level.name}</h3>
                  <span className="badge badge-beginner">
                    {level.passThreshold}% to pass
                  </span>
                </div>
                <p>{level.description}</p>
                <p className="hint">{level.signCount} signs covered</p>
                <button
                  type="button"
                  className="btn-accent"
                  style={{ marginTop: 14 }}
                  onClick={() => startExam(level)}
                >
                  Start {level.name} Exam
                </button>
              </div>
            ))}
          </div>

          <p className="section-heading" style={{ marginTop: 32 }}>
            <span className="icon">📜</span> Your Exam History
          </p>

          {mockHistory.length === 0 ? (
            <p className="lessons-status">
              You haven't taken a certification exam yet.
            </p>
          ) : (
            <div className="report-panel">
              <div className="table-scroll">
                <table className="attempts-table">
                  <thead>
                    <tr>
                      <th>Level</th>
                      <th>Score</th>
                      <th>Result</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockHistory.map((attempt) => (
                      <tr key={attempt.id}>
                        <td>{attempt.level}</td>
                        <td>{attempt.score}%</td>
                        <td>
                          <span
                            className={
                              attempt.passed
                                ? "status-badge"
                                : "status-badge low"
                            }
                          >
                            {attempt.passed ? "Passed" : "Not passed"}
                          </span>
                        </td>
                        <td>{attempt.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {examState === "in-progress" && selectedLevel && (
        <div className="report-panel">
          <p className="panel-title">{selectedLevel.name} Exam — In Progress</p>
          <p className="page-sub">
            This is a placeholder exam flow. The real version will step
            through {selectedLevel.signCount} signs using the webcam, the
            same way Practice does, then submit all attempts together for
            scoring.
          </p>
          <button type="button" className="btn-primary" onClick={finishMockExam}>
            Finish Exam (Demo)
          </button>
          <button
            type="button"
            className="btn-secondary btn-inline"
            style={{ marginTop: 10 }}
            onClick={resetExam}
          >
            Cancel
          </button>
        </div>
      )}

      {examState === "result" && mockResult && (
        <div className="report-panel">
          <p className="panel-title">Exam Result</p>
          <div className="summary-row">
            <span>Level</span>
            <span>{selectedLevel.name}</span>
          </div>
          <div className="summary-row">
            <span>Score</span>
            <span>{mockResult.score}%</span>
          </div>
          <div className="summary-row">
            <span>Pass threshold</span>
            <span>{selectedLevel.passThreshold}%</span>
          </div>

          {mockResult.passed ? (
            <p className="certificate-note" style={{ marginTop: 12 }}>
              🎉 You passed! A certificate for this level would be generated
              here once connected to the real certificate endpoint.
            </p>
          ) : (
            <p className="certificate-locked" style={{ marginTop: 12 }}>
              You didn't reach the pass threshold this time. Practice the
              weaker signs and try again.
            </p>
          )}

          <button
            type="button"
            className="btn-secondary btn-inline"
            style={{ marginTop: 14 }}
            onClick={resetExam}
          >
            Back to Exam Levels
          </button>
        </div>
      )}
    </div>
  );
}