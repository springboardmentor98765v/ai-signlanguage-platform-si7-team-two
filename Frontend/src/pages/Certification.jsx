import { useState, useEffect, useRef } from "react";
import {
  predictSign,
  submitCertificationExam,
  downloadExamCertificate,
} from "../services/api.js";
import { getUser } from "../utils/auth.js";

const LEVELS = [
  {
    id: "beginner",
    name: "Beginner",
    description: "Covers signs A through E.",
    passThreshold: 70,
    signs: ["A", "B", "C", "D", "E"],
  },
  {
    id: "intermediate",
    name: "Intermediate",
    description: "Covers signs F through M.",
    passThreshold: 75,
    signs: ["F", "G", "H", "I", "J", "K", "L", "M"],
  },
  {
    id: "advanced",
    name: "Advanced",
    description: "Covers signs N through U.",
    passThreshold: 80,
    signs: ["N", "O", "P", "Q", "R", "S", "T", "U"],
  },
  {
    id: "professional",
    name: "Professional",
    description: "Covers signs V through Z.",
    passThreshold: 85,
    signs: ["V", "W", "X", "Y", "Z"],
  },
];

export default function Certification() {
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [examState, setExamState] = useState("idle");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [examResults, setExamResults] = useState([]);
  const [isPracticing, setIsPracticing] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [finalResult, setFinalResult] = useState(null);

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);

  const targetLetter = selectedLevel ? selectedLevel.signs[currentIndex] : null;

  useEffect(() => {
    return () => {
      stopStream();
    };
  }, []);

  useEffect(() => {
    if (isPracticing && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
      videoRef.current.onloadedmetadata = async () => {
        try {
          await videoRef.current.play();
        } catch (e) {
          console.error(e);
        }
      };
    }
  }, [isPracticing]);

  function stopStream() {
    if (!streamRef.current) return;
    streamRef.current.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  }

  async function startExam(level) {
    setSelectedLevel(level);
    setExamState("in-progress");
    setCurrentIndex(0);
    setExamResults([]);
    setFinalResult(null);
    setSubmitError("");
    setCameraError("");
  }

  async function handleStartCamera() {
    setCameraError("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: "user" },
        audio: false,
      });
      streamRef.current = stream;
      setIsPracticing(true);
    } catch (err) {
      console.error(err);
      setCameraError("Camera access denied or unavailable. Please allow camera permission.");
      setIsPracticing(false);
    }
  }

  async function handleCheckSign() {
    if (!videoRef.current || !targetLetter) return;

    setIsChecking(true);
    try {
      const canvas = canvasRef.current;
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      canvas.getContext("2d").drawImage(videoRef.current, 0, 0);

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg")
      );

      if (!blob) throw new Error("Unable to capture webcam frame.");

      const predictionResult = await predictSign(blob);

      const predictedSign =
        predictionResult.prediction ?? predictionResult.predicted_sign;
      const isCorrect = predictedSign === targetLetter;
      const accuracy = isCorrect ? predictionResult.confidence : 0;

      const newResults = [...examResults, { letter: targetLetter, accuracy }];
      setExamResults(newResults);

      if (currentIndex + 1 < selectedLevel.signs.length) {
        setCurrentIndex(currentIndex + 1);
      } else {
        stopStream();
        setIsPracticing(false);
        await finishExam(newResults);
      }
    } catch (err) {
      console.error(err);
      setCameraError(err.message || "Could not check your sign.");
    } finally {
      setIsChecking(false);
    }
  }

  async function finishExam(results) {
    setExamState("submitting");
    const user = getUser();
    if (!user) {
      setSubmitError("You must be logged in to submit an exam.");
      setExamState("result");
      return;
    }

    try {
      const scores = results.map((r) => r.accuracy);
      const response = await submitCertificationExam(
        user.id,
        selectedLevel.name,
        scores
      );
      setFinalResult(response);
      setExamState("result");
    } catch (err) {
      setSubmitError(err.message || "Failed to submit exam results.");
      setExamState("result");
    }
  }

  function resetExam() {
    stopStream();
    setSelectedLevel(null);
    setExamState("idle");
    setCurrentIndex(0);
    setExamResults([]);
    setFinalResult(null);
    setSubmitError("");
    setCameraError("");
    setIsPracticing(false);
    setIsChecking(false);
  }

  async function handleDownloadCertificate() {
    if (!finalResult || !finalResult.exam_id) return;
    try {
      const blob = await downloadExamCertificate(finalResult.exam_id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Certificate_${getUser()?.full_name || "Learner"}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Failed to download certificate:", err);
    }
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
                <p className="hint">{level.signs.length} signs covered</p>
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
        </>
      )}

      {examState === "in-progress" && selectedLevel && (
        <div className="report-panel">
          <p className="panel-title">
            {selectedLevel.name} Exam — In Progress
          </p>
          <p className="page-sub">
            Sign the letter shown below. Question {currentIndex + 1} of{" "}
            {selectedLevel.signs.length}.
          </p>

          <div className="practice-grid">
            <div className="practice-panel">
              <div className="video-frame">
                {isPracticing ? (
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="video-feed"
                  />
                ) : (
                  <div className="video-placeholder">Camera is Off</div>
                )}
              </div>

              <canvas ref={canvasRef} style={{ display: "none" }} />
              {cameraError && (
                <p className="camera-error" role="alert">
                  {cameraError}
                </p>
              )}

              <div className="practice-controls">
                {!isPracticing ? (
                  <button
                    className="btn-primary"
                    onClick={handleStartCamera}
                  >
                    Start Camera
                  </button>
                ) : (
                  <button
                    className="btn-check"
                    onClick={handleCheckSign}
                    disabled={isChecking}
                  >
                    {isChecking ? "Checking…" : "Submit Sign"}
                  </button>
                )}
              </div>
            </div>

            <div className="practice-side">
              <div
                className="reference-card"
                style={{
                  textAlign: "center",
                  padding: "40px 20px",
                }}
              >
                <p className="label">Current Target Sign</p>
                <h1 style={{ fontSize: "72px", margin: "20px 0" }}>
                  {targetLetter}
                </h1>
                <p className="hint">
                  Make this sign and click &quot;Submit Sign&quot;.
                </p>
              </div>
            </div>
          </div>

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

      {(examState === "result" || examState === "submitting") && (
        <div className="report-panel">
          <p className="panel-title">Exam Result</p>

          {examState === "submitting" && (
            <p>Submitting results...</p>
          )}

          {submitError && (
            <p className="camera-error">{submitError}</p>
          )}

          {finalResult && (
            <>
              <div className="summary-row">
                <span>Level</span>
                <span>{selectedLevel?.name}</span>
              </div>
              <div className="summary-row">
                <span>Score</span>
                <span>{finalResult.score?.toFixed(2)}%</span>
              </div>
              <div className="summary-row">
                <span>Pass threshold</span>
                <span>{selectedLevel?.passThreshold}%</span>
              </div>

              {finalResult.is_passed ? (
                <>
                  <p
                    className="certificate-note"
                    style={{ marginTop: 12 }}
                  >
                    🎉 You passed! Download your certificate below.
                  </p>
                  <button
                    type="button"
                    className="btn-accent"
                    style={{ marginTop: 14 }}
                    onClick={handleDownloadCertificate}
                  >
                    Download Certificate
                  </button>
                </>
              ) : (
                <p
                  className="certificate-locked"
                  style={{ marginTop: 12 }}
                >
                  You didn&apos;t reach the pass threshold this time.
                  Practice the weaker signs and try again.
                </p>
              )}
            </>
          )}

          {!finalResult && !submitError && examState === "result" && (
            <p>Processing result...</p>
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
