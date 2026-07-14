import { useRef, useState, useEffect } from "react";
import { predictSign, assessAttempt } from "../services/api.js";

export default function Practice() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);

  const [isPracticing, setIsPracticing] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [targetLetter] = useState("A");

  const [isChecking, setIsChecking] = useState(false);
  const [checkError, setCheckError] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [assessment, setAssessment] = useState(null);

  // Attach camera stream after video element is rendered
  useEffect(() => {
    if (
        isPracticing &&
        videoRef.current &&
        streamRef.current
    ) {
        videoRef.current.srcObject = streamRef.current;

        videoRef.current.onloadedmetadata = async () => {
            try {
                await videoRef.current.play();
            } catch (err) {
                console.error(err);
            }
        };
    }
}, [isPracticing]);
useEffect(() => {
    return () => {
        stopStream();
    };
}, []);
  function stopStream() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }

  async function handleStart() {
    setCameraError("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });

      streamRef.current = stream;

      // DO NOT attach stream here
      setIsPracticing(true);
    } catch (err) {
      console.error(err);

      setCameraError(
        "Camera access denied or unavailable. Please allow camera permission and try again."
      );

      setIsPracticing(false);
    }
  }

  function handleStop() {
    stopStream();

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsPracticing(false);
  }

  async function handleCheckSign() {
    if (!videoRef.current) return
    setCheckError('')
    setIsChecking(true)
    setPrediction(null)
    setAssessment(null)
    const attemptStartedAt = performance.now()

    try {
      const canvas = canvasRef.current;

      console.log("Video Width:", videoRef.current.videoWidth);
      console.log("Video Height:", videoRef.current.videoHeight);

      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;

      const ctx = canvas.getContext("2d");

      ctx.drawImage(
        videoRef.current,
        0,
        0,
        canvas.width,
        canvas.height
      );

      const blob = await new Promise((resolve, reject) => {
        canvas.toBlob((blob) => {
          if (blob) {
            resolve(blob);
          } else {
            reject(new Error("Failed to capture webcam frame."));
          }
        }, "image/jpeg");
      });

      const predictionResult = await predictSign(blob);

      console.log(predictionResult);

      setPrediction(predictionResult);

      const assessmentResult = await assessAttempt(
        targetLetter,
        predictionResult.predicted_sign,
        predictionResult.confidence,
        (performance.now() - attemptStartedAt) / 1000
      )
      setAssessment(assessmentResult)
    } catch (err) {
      console.error(err);

      setCheckError(
        err.message || "Could not check your sign. Please try again."
      );
    } finally {
      setIsChecking(false);
    }
  }

  return (
    <div>
      <div className="practice-header">
        <h2>Practice: Letter {targetLetter}</h2>
        <p className="sub">
          Show the sign in front of your camera and hold it steady.
        </p>
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
              <div className="video-placeholder">
                <span>Camera is off</span>
              </div>
            )}
          </div>

          <canvas
            ref={canvasRef}
            style={{ display: "none" }}
          />

          {cameraError && (
            <p className="camera-error">{cameraError}</p>
          )}

          {checkError && (
            <p className="camera-error">{checkError}</p>
          )}

          <div className="practice-controls">
            {!isPracticing ? (
              <button
                className="btn-primary"
                onClick={handleStart}
              >
                Start Practice
              </button>
            ) : (
              <>
                <button
                  className="btn-stop"
                  onClick={handleStop}
                >
                  Stop Practice
                </button>

                <button
                  className="btn-check"
                  onClick={handleCheckSign}
                  disabled={isChecking}
                >
                  {isChecking
                    ? "Checking..."
                    : "Check My Sign"}
                </button>
              </>
            )}
          </div>

          {assessment && (
            <div className="result-card">
              <div className="assessment-summary">
                <p className="label">Assessment Summary</p>
                <div className="summary-grid">
                  <div className="summary-item"><span>Letter</span><strong>{assessment.expected_sign}</strong></div>
                  <div className="summary-item"><span>Prediction</span><strong>{assessment.predicted_sign}</strong></div>
                  <div className="summary-item"><span>Result</span><strong className={assessment.is_correct ? 'correct' : 'incorrect'}>{assessment.is_correct ? '✓ Correct' : '✕ Incorrect'}</strong></div>
                  <div className="summary-item"><span>Status</span><strong>{assessment.status}</strong></div>
                  <div className="summary-item"><span>Attempt time</span><strong>{assessment.attempt_duration}s</strong></div>
                  <div className="summary-item"><span>Completed at</span><strong>{new Date(assessment.completed_at).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}</strong></div>
                </div>
                <div className="metric-row">
                  <span>Confidence</span>
                  <div className="progress-track"><div className="progress-fill" style={{ width: `${assessment.confidence}%` }} /></div>
                  <strong>{assessment.confidence}%</strong>
                </div>
                <div className="metric-row">
                  <span>Accuracy</span>
                  <div className="progress-track"><div className="progress-fill" style={{ width: `${assessment.accuracy}%` }} /></div>
                  <strong>{assessment.accuracy}%</strong>
                </div>
              </div>

              <ul className="feedback-list">
                {assessment.feedback.map((msg, i) => (
                  <li key={i}><span aria-hidden="true">✓</span>{msg}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="practice-side">
          <div className="reference-card">
            <p className="label">
              Reference Sign
            </p>

            <div className="reference-image">
              <span>{targetLetter}</span>
            </div>

            <p className="hint">
              Match your hand shape to this reference.
            </p>
          </div>

          <div className="prediction-card">
            <p className="label">
              AI Prediction
            </p>

            <div className="prediction-placeholder">
              <p className="predicted-sign">
                {prediction
                  ? prediction.prediction
                  : "--"}
              </p>

              <p className="confidence">
                Confidence:{" "}
                {prediction
                  ? `${prediction.confidence}%`
                  : "--%"}
              </p>
            </div>

            <p className="hint">
              Prediction updates each time you click
              "Check My Sign".
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}