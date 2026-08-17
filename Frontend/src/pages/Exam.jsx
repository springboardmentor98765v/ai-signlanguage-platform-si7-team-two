import { useRef, useState, useEffect } from "react";
import {
  predictSign,
  submitCertificationExam
} from "../services/api.js";
import { useNavigate } from "react-router-dom";
import { getUser } from "../utils/auth.js";
import CelebrationOverlay from "../components/celebrations/CelebrationOverlay.jsx";

const EXAM_LETTERS = ["A", "B", "C", "D", "E"]; // Fixed exam sequence for MVP

export default function Exam() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [examResults, setExamResults] = useState([]); // Array of accuracies
  const [isPracticing, setIsPracticing] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [isChecking, setIsChecking] = useState(false);
  const [examComplete, setExamComplete] = useState(false);
  const [finalScore, setFinalScore] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const targetLetter = EXAM_LETTERS[currentIndex];

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

      const predictionResult = await predictSign(blob, targetLetter);
      
      const predictedSign = predictionResult.prediction ?? predictionResult.predicted_sign;
      const isCorrect = predictedSign === targetLetter;
      const accuracy = isCorrect ? predictionResult.confidence : 0; // Simple scoring

      const newResults = [...examResults, { letter: targetLetter, accuracy }];
      setExamResults(newResults);

      if (currentIndex + 1 < EXAM_LETTERS.length) {
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
    const totalScore = results.reduce((acc, curr) => acc + curr.accuracy, 0) / results.length;
    setFinalScore(totalScore);

    const user = getUser();
    if (user) {
      setSubmitting(true);
      try {
        await submitCertificationExam(user.id, { score: totalScore });
      } catch (err) {
        console.error("Failed to submit exam:", err);
        setSubmitError("Failed to submit exam results.");
      } finally {
        setSubmitting(false);
      }
    }
  }

  if (examComplete) {
    return (
      <div>
        <h1 className="sr-only">Certification Exam</h1>
        <div className="reports-header">
          <h2>Exam Complete</h2>
          <p className="sub">You have finished the certification exam.</p>
        </div>
        
        <div className="report-panel" style={{ marginTop: '24px' }}>
          <h3>Final Score: {finalScore ? finalScore.toFixed(2) : '--'}%</h3>
          {submitting && <p>Submitting results...</p>}
          {submitError && <p className="camera-error">{submitError}</p>}
          {!submitting && !submitError && (
            <p>Your results have been recorded. If you scored 80% or higher, you may be eligible for a certificate!</p>
          )}
          
          <button className="btn-primary" onClick={() => navigate('/reports')} style={{ marginTop: '16px' }}>
            Go to Reports
          </button>
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
              Sign the letters shown below. Question {currentIndex + 1} of {EXAM_LETTERS.length}.
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
              <button className="btn-primary" onClick={handleStart}>
                Start Exam
              </button>
            ) : (
              <button
                className="btn-check"
                onClick={handleCheckSign}
                disabled={isChecking}
              >
                {isChecking ? 'Checking…' : 'Submit Sign'}
              </button>
            )}
          </div>
        </div>

        <div className="practice-side">
          <div className="reference-card" style={{ textAlign: 'center', padding: '40px 20px' }}>
            <p className="label">Current Target Letter</p>
            <h1 style={{ fontSize: '72px', margin: '20px 0' }}>{targetLetter}</h1>
            <p className="hint">Make this sign and click 'Submit Sign'.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
