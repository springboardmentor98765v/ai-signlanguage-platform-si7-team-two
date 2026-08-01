import { useRef, useState, useEffect } from "react";
import {
  predictSign,
  assessAttempt,
  getLessons,
  startPracticeSession,
  endPracticeSession,
} from "../services/api.js";
import { useParams, useNavigate } from "react-router-dom";
import { getUser } from "../utils/auth.js";

const TARGET_ATTEMPTS = 5;

function getStatusLabel(accuracy) {
  if (accuracy >= 90) return "Excellent";
  if (accuracy >= 75) return "Good";
  if (accuracy >= 50) return "Fair";
  return "Needs Practice";
}

function formatTime(totalSeconds) {
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

export default function Practice() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  const [isPracticing, setIsPracticing] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [lessonList, setLessonList] = useState([]);
  const { letter } = useParams();

  useEffect(() => {
    async function loadLessons() {
      try {
        const data = await getLessons();
        setLessonList(data);
      } catch (err) {
        console.error("Failed to load lessons:", err);
        setLessonList([]);
      }
    }

    loadLessons();
  }, []);

  const targetLetter = letter || "A";

  const [isChecking, setIsChecking] = useState(false);
  const [checkError, setCheckError] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [assessment, setAssessment] = useState(null);
  const [attemptTime, setAttemptTime] = useState(null);

  const [sessionId, setSessionId] = useState(null);
  const sessionIdRef = useRef(null);

  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [attemptCount, setAttemptCount] = useState(0);
  const timerRef = useRef(null);

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

  useEffect(() => {
    if (isPracticing) {
      timerRef.current = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    } else if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPracticing]);

  useEffect(() => {
    return () => {
      stopStream();
      if (sessionIdRef.current) {
        endPracticeSession(sessionIdRef.current).catch(() => {});
      }
    };
  }, []);

  function stopStream() {
    if (!streamRef.current) return;

    streamRef.current.getTracks().forEach((track) => track.stop());

    streamRef.current = null;
  }

  function handleLetterChange(e) {
    setPrediction(null);
    setAssessment(null);
    setAttemptTime(null);
    setAttemptCount(0);
    navigate(`/practice/${e.target.value}`);
  }

  async function handleStart() {
    setCameraError("");
    setElapsedSeconds(0);
    setAttemptCount(0);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
          facingMode: "user",
        },
        audio: false,
      });

      console.log("Camera Stream:", stream);

      streamRef.current = stream;

      setIsPracticing(true);

      try {
        const user = getUser();
        const lesson = lessonList.find((l) => l.letter === targetLetter);

        if (user && lesson) {
          const session = await startPracticeSession(user.id, lesson.id);
          setSessionId(session.session_id);
          sessionIdRef.current = session.session_id;
        } else {
          console.warn(
            "Could not start a practice session (missing user or lesson) — attempts won't be saved.",
          );
        }
      } catch (err) {
        console.error("Failed to start practice session:", err);
      }
    } catch (err) {
      console.error(err);

      setCameraError(
        "Camera access denied or unavailable. Please allow camera permission.",
      );

      setIsPracticing(false);
    }
  }

  async function handleStop() {
    stopStream();

    if (videoRef.current) videoRef.current.srcObject = null;

    setIsPracticing(false);

    if (sessionIdRef.current) {
      try {
        await endPracticeSession(sessionIdRef.current);
      } catch (err) {
        console.error("Failed to end practice session:", err);
      } finally {
        setSessionId(null);
        sessionIdRef.current = null;
      }
    }
  }

  async function handleCheckSign() {
    if (!videoRef.current) return;

    setCheckError("");
    setIsChecking(true);
    setPrediction(null);
    setAssessment(null);
    setAttemptTime(null);

    const startedAt = performance.now();

    try {
      const canvas = canvasRef.current;

      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;

      canvas.getContext("2d").drawImage(videoRef.current, 0, 0);

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg"),
      );

      if (!blob) {
        throw new Error("Unable to capture webcam frame.");
      }

      const predictionResult = await predictSign(blob);

      setPrediction(predictionResult);

      const assessmentResult = await assessAttempt(
        sessionIdRef.current,
        targetLetter,
        predictionResult.prediction ?? predictionResult.predicted_sign,
        predictionResult.confidence,
      );

      setAssessment(assessmentResult);

      const elapsed = ((performance.now() - startedAt) / 1000).toFixed(1);

      setAttemptTime(elapsed);
      setAttemptCount((prev) => Math.min(prev + 1, TARGET_ATTEMPTS));
    } catch (err) {
      console.error(err);
      setCheckError(err.message || "Could not check your sign.");
    } finally {
      setIsChecking(false);
    }
  }

  const isCorrect =
    prediction &&
    (prediction.prediction ?? prediction.predicted_sign) === targetLetter;

  const statusLabel = assessment
    ? assessment.status || getStatusLabel(assessment.accuracy)
    : null;

  const progressPercent = Math.min(
    (attemptCount / TARGET_ATTEMPTS) * 100,
    100,
  );

  return (
    <div>
      <div className="practice-header">
        <div className="practice-header-row">
          <div>
            <h2>Practice: Letter {targetLetter}</h2>
            <p className="sub">
              Show the sign in front of your camera and hold it steady.
            </p>
          </div>

          <div className="letter-picker">
            <label htmlFor="letter-select">Pick a letter</label>
            <select id="letter-select" value={targetLetter} onChange={handleLetterChange}>
              {lessonList.length === 0 ? (
                <option value={targetLetter}>{targetLetter}</option>
              ) : (
                lessonList.map((l) => (
                  <option key={l.id} value={l.letter}>
                    {l.title}
                    {l.difficulty ? ` · ${l.difficulty}` : ""}
                  </option>
                ))
              )}
            </select>
          </div>
        </div>
      </div>

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
                aria-label="Live camera preview of your hand sign"
              />
            ) : (
              <div className="video-placeholder">Camera is Off</div>
            )}

            {isPracticing && (
              <div className="session-timer">{formatTime(elapsedSeconds)}</div>
            )}
          </div>

          <canvas ref={canvasRef} style={{ display: "none" }} />

          {cameraError && <p className="camera-error" role="alert">{cameraError}</p>}

          {checkError && <p className="camera-error" role="alert">{checkError}</p>}

          {isPracticing && (
            <div className="attempt-progress">
              <div className="attempt-progress-label">
                <span>Attempt {Math.min(attemptCount, TARGET_ATTEMPTS)} of {TARGET_ATTEMPTS}</span>
              </div>
              <div className="attempt-progress-bar-wrap">
                <div
                  className="attempt-progress-bar"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>
          )}

          <div className="practice-controls">
            {!isPracticing ? (
              <button className="btn-primary" onClick={handleStart}>
                Start Practice
              </button>
            ) : (
              <>
                <button className="btn-stop" onClick={handleStop}>
                  Stop Practice
                </button>

                <button
                  className="btn-check"
                  onClick={handleCheckSign}
                  disabled={isChecking}
                >
                  {isChecking ? "Checking..." : "Check My Sign"}
                </button>
              </>
            )}
          </div>

          {assessment && (
            <div role="status" aria-live="polite">
              <div className="practice-result-row">
                <div>
                  <p className="label">Letter</p>
                  <p>{targetLetter}</p>
                </div>

                <div>
                  <p className="label">Prediction</p>
                  <p>{prediction.prediction ?? prediction.predicted_sign}</p>
                </div>

                <div>
                  <p className="label">Result</p>

                  <p
                    className={
                      isCorrect ? "result-correct" : "result-incorrect"
                    }
                  >
                    {isCorrect ? "✔️ Correct" : "❌ Incorrect"}
                  </p>
                </div>
              </div>

              <div className="summary-card">
                <div className="summary-row">
                  <span>Confidence</span>
                  <span>{prediction.confidence}%</span>
                </div>

                <div className="summary-row">
                  <span>Accuracy</span>
                  <span>{assessment.accuracy}%</span>
                </div>

                <div className="summary-row">
                  <span>Status</span>
                  <span>{statusLabel}</span>
                </div>

                {attemptTime && (
                  <div className="summary-row">
                    <span>Attempt Time</span>
                    <span>{attemptTime}s</span>
                  </div>
                )}
              </div>

              <div className={`feedback-panel ${isCorrect ? "feedback-good" : "feedback-warn"}`}>
                <p className="feedback-panel-title">
                  {isCorrect ? "Nice work" : "Correction tips"}
                </p>
                <ul className="feedback-list">
                  {assessment?.feedback?.length ? (
                    assessment.feedback.map((msg, i) => (
                      <li key={i}>
                        <span className="feedback-icon">{isCorrect ? "✓" : "•"}</span>
                        {msg}
                      </li>
                    ))
                  ) : (
                    <li>
                      <span className="feedback-icon">•</span>
                      No feedback available.
                    </li>
                  )}
                </ul>
              </div>
            </div>
          )}
        </div>

        <div className="practice-side">
          <div className="reference-card">
            <p className="label">Reference Sign</p>

            <div className="reference-image">
              <span>{targetLetter}</span>
            </div>

            <p className="hint">Match your hand shape.</p>
          </div>

          <div className="prediction-card">
            <p className="label">AI Prediction</p>

            <div className="prediction-placeholder">
              <p className="predicted-sign">
                {prediction
                  ? (prediction.prediction ?? prediction.predicted_sign)
                  : "--"}
              </p>

              <p className="confidence">
                Confidence:
                {prediction ? ` ${prediction.confidence}%` : " --%"}
              </p>
              {prediction && (
                <>
                  <p className="label" style={{ marginTop: "12px" }}>
                    Possible Issue
                  </p>

                  <p className="possible-issue">{prediction.possible_issue}</p>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}