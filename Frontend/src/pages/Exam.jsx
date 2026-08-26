import { useRef, useState, useEffect } from "react";
import {
  predictSign,
  submitCertificationExam,
  getExamLetters,
  getExamCertificate,
} from "../services/api.js";
import { useNavigate } from "react-router-dom";
import { getUser } from "../utils/auth.js";
import CelebrationOverlay from "../components/celebrations/CelebrationOverlay.jsx";

// Default to a "Full" level that drives the backend to return all 26 letters.
// The actual set is fetched from /certification_exams/letters?level=Full on mount.
const EXAM_LEVEL = "Full";

export default function Exam() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  const [examLetters, setExamLetters] = useState([]); // populated from backend
  const [examLevel, setExamLevel] = useState(EXAM_LEVEL);
  const [passThreshold, setPassThreshold] = useState(80.0);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [examResults, setExamResults] = useState([]); // Array of {letter, confidence, predictedSign, isCorrect}
  const [isPracticing, setIsPracticing] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [isChecking, setIsChecking] = useState(false);
  const [examComplete, setExamComplete] = useState(false);
  const [finalScore, setFinalScore] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [examSubmission, setExamSubmission] = useState(null); // { is_passed, exam_id, certificate_id }
  const [certificateStatus, setCertificateStatus] = useState(""); // idle | loading | error
  const [certificateError, setCertificateError] = useState("");

  const targetLetter = examLetters[currentIndex];

  // Fetch the letter set on mount. Backend decides the actual sequence
  // (currently all 26 letters for level=Full), frontend just consumes it.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const { level, letters, passThreshold: threshold } =
        await getExamLetters(EXAM_LEVEL);
      if (cancelled) return;
      setExamLevel(level);
      setExamLetters(letters);
      setPassThreshold(threshold);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

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

  function saveBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function handleStart() {
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
    if (!videoRef.current) return;
    if (!targetLetter) return;

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

      // Read the AI's REAL prediction and confidence. predictSign already
      // wraps retry + demo fallback, so this is the most honest signal we
      // have about what the model thought the learner signed.
      const predictionResult = await predictSign(blob, targetLetter);

      const predictedSign = predictionResult.prediction ?? predictionResult.predicted_sign;
      const rawConfidence = Number(predictionResult.confidence) || 0;
      const isCorrect = predictedSign === targetLetter;

      // Per-letter score: use the AI's actual confidence as the score.
      // If the prediction was wrong, score is 0 — the learner gets no
      // credit for a wrong sign, regardless of confidence on the wrong label.
      const score = isCorrect ? Math.max(0, Math.min(100, rawConfidence)) : 0;

      const newResults = [
        ...examResults,
        { letter: targetLetter, predictedSign, confidence: rawConfidence, score, isCorrect },
      ];
      setExamResults(newResults);

      if (currentIndex + 1 < examLetters.length) {
        setCurrentIndex(currentIndex + 1);
      } else {
        // Exam is complete
        stopStream();
        setIsPracticing(false);
        setExamComplete(true);
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
    // Final score is the simple mean of per-letter scores (each 0-100).
    const totalScore =
      results.reduce((acc, curr) => acc + (Number(curr.score) || 0), 0) /
      results.length;
    setFinalScore(totalScore);

    const user = getUser();
    if (!user) {
      setSubmitError("Sign-in required to record your exam results.");
      return;
    }

    // Match the Pydantic schema in Bussiness_Logic/routers/certification_exam.py
    // ExamSubmission { learner_id, level, scores: List[float] }.
    const payload = {
      learner_id: user.id,
      level: examLevel,
      scores: results.map((r) => Number(r.score) || 0),
    };

    setSubmitting(true);
    try {
      const result = await submitCertificationExam(user.id, payload);
      setExamSubmission(result);
    } catch (err) {
      console.error("Failed to submit exam:", err);
      setSubmitError(
        err?.message || "Failed to submit exam results. Please try again."
      );
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDownloadCertificate() {
    if (!examSubmission?.exam_id) return;
    setCertificateStatus("loading");
    setCertificateError("");
    try {
      const blob = await getExamCertificate(examSubmission.exam_id);
      const user = getUser();
      const learnerName = (user?.name || user?.full_name || "Learner").replace(
        /\s+/g,
        "_"
      );
      saveBlob(blob, `Certificate_${learnerName}.pdf`);
      setCertificateStatus("");
    } catch (err) {
      console.error("Certificate download failed:", err);
      setCertificateError(
        err?.message || "Could not download your certificate. Please try again."
      );
      setCertificateStatus("error");
    }
  }

  if (examComplete) {
    const isPassed =
      examSubmission?.is_passed ?? (finalScore != null && finalScore >= passThreshold);
    const hasExamId = Boolean(examSubmission?.exam_id);

    return (
      <div>
        <h1 className="sr-only">Certification Exam</h1>
        <div className="reports-header">
          <h2>Exam Complete</h2>
          <p className="sub">You have finished the {examLevel} certification exam.</p>
        </div>

        <div className="report-panel" style={{ marginTop: '24px' }}>
          <h3>Final Score: {finalScore != null ? finalScore.toFixed(2) : '--'}%</h3>
          <p>
            Pass threshold: <strong>{passThreshold.toFixed(1)}%</strong> &middot;{" "}
            <strong>{isPassed ? 'Passed ✅' : 'Did not pass ❌'}</strong>
          </p>

          {submitting && <p>Submitting results...</p>}
          {submitError && <p className="camera-error" role="alert">{submitError}</p>}

          {!submitting && !submitError && isPassed && (
            <p>Congratulations! Your certificate has been generated.</p>
          )}
          {!submitting && !submitError && !isPassed && (
            <p>
              You didn&apos;t reach the pass threshold this time. Keep practicing
              and try again — your previous lessons are still recorded.
            </p>
          )}

          <div style={{ marginTop: '20px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            {isPassed && hasExamId && (
              <button
                className="btn-primary"
                onClick={handleDownloadCertificate}
                disabled={certificateStatus === "loading"}
              >
                {certificateStatus === "loading"
                  ? "Preparing your certificate..."
                  : "Download Certificate (PDF)"}
              </button>
            )}
            <button
              className="btn-secondary btn-inline"
              onClick={() => navigate('/reports')}
            >
              Go to Reports
            </button>
          </div>

          {certificateStatus === "error" && certificateError && (
            <p className="camera-error" role="alert" style={{ marginTop: '12px' }}>
              {certificateError}
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="sr-only">Certification Exam</h1>
      <div className="practice-header">
        <div className="practice-header-row">
          <div>
            <h2>Certification Exam</h2>
            <p className="sub">
              {examLetters.length > 0
                ? `Sign the letters shown below. Question ${currentIndex + 1} of ${examLetters.length}.`
                : "Loading exam sequence…"}
            </p>
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
              />
            ) : (
              <div className="video-placeholder">Camera is Off</div>
            )}
          </div>

          <canvas ref={canvasRef} style={{ display: "none" }} />
          {cameraError && <p className="camera-error" role="alert">{cameraError}</p>}

          <div className="practice-controls">
            {!isPracticing ? (
              <button
                className="btn-primary"
                onClick={handleStart}
                disabled={examLetters.length === 0}
              >
                Start Exam
              </button>
            ) : (
              <button
                className="btn-check"
                onClick={handleCheckSign}
                disabled={isChecking || !targetLetter}
              >
                {isChecking ? 'Checking…' : 'Submit Sign'}
              </button>
            )}
          </div>
        </div>

        <div className="practice-side">
          <div className="reference-card" style={{ textAlign: 'center', padding: '40px 20px' }}>
            <p className="label">Current Target Letter</p>
            <h1 style={{ fontSize: '72px', margin: '20px 0' }}>
              {targetLetter || "—"}
            </h1>
            <p className="hint">Make this sign and click 'Submit Sign'.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
