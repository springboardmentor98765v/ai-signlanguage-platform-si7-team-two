import { useRef, useState, useEffect } from 'react'
import { predictSign, assessAttempt } from '../services/api.js'
import { useParams } from "react-router-dom";
import { useLocation } from 'react-router-dom'
function getStatusLabel(accuracy) {
  if (accuracy >= 90) return 'Excellent'
  if (accuracy >= 75) return 'Good'
  if (accuracy >= 50) return 'Fair'
  return 'Needs Practice'
}

export default function Practice() {
  
  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const canvasRef = useRef(null)

  const [isPracticing, setIsPracticing] = useState(false)
  const [cameraError, setCameraError] = useState('')
  const { letter } = useParams();

const targetLetter = letter || "A";

  const [isChecking, setIsChecking] = useState(false)
  const [checkError, setCheckError] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [assessment, setAssessment] = useState(null)
  const [attemptTime, setAttemptTime] = useState(null)

  // Attach stream AFTER the video element is rendered
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

            } catch (e) {

                console.error(e);

            }

        };

    }

}, [isPracticing]);


// Cleanup ONLY when component unmounts

useEffect(() => {

    return () => {

        stopStream();

    };

}, []);
  function stopStream() {

    if (!streamRef.current)
        return;

    streamRef.current
        .getTracks()
        .forEach(track => track.stop());

    streamRef.current = null;

}

  async function handleStart() {
    setCameraError('')

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
          facingMode: "user"
        },
        audio: false
      })

      console.log("Camera Stream:", stream)

      streamRef.current = stream

      setIsPracticing(true)

    } catch (err) {
      console.error(err)

      setCameraError(
        'Camera access denied or unavailable. Please allow camera permission.'
      )

      setIsPracticing(false)
    }
  }

  function handleStop() {

    stopStream();

    if (videoRef.current)
        videoRef.current.srcObject = null;

    setIsPracticing(false);

}

  async function handleCheckSign() {
    if (!videoRef.current) return

    setCheckError('')
    setIsChecking(true)
    setPrediction(null)
    setAssessment(null)
    setAttemptTime(null)

    const startedAt = performance.now()

    try {
      const canvas = canvasRef.current

      canvas.width = videoRef.current.videoWidth
      canvas.height = videoRef.current.videoHeight

      canvas
        .getContext('2d')
        .drawImage(videoRef.current, 0, 0)

      const blob = await new Promise(resolve =>
        canvas.toBlob(resolve, 'image/jpeg')
      )

      if (!blob) {
        throw new Error("Unable to capture webcam frame.")
      }

      const predictionResult = await predictSign(blob)

      setPrediction(predictionResult)

      const assessmentResult = await assessAttempt(
        targetLetter,
        predictionResult.prediction ?? predictionResult.predicted_sign,
        predictionResult.confidence
      )

      setAssessment(assessmentResult)

      const elapsedSeconds =
        ((performance.now() - startedAt) / 1000).toFixed(1)

      setAttemptTime(elapsedSeconds)

    } catch (err) {
      console.error(err)
      setCheckError(
        err.message || 'Could not check your sign.'
      )
    } finally {
      setIsChecking(false)
    }
  }

  const isCorrect =
    prediction &&
    (prediction.prediction ?? prediction.predicted_sign) === targetLetter

  const statusLabel =
    assessment
      ? (assessment.status || getStatusLabel(assessment.accuracy))
      : null

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
                Camera is Off
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
                  {isChecking ? "Checking..." : "Check My Sign"}
                </button>
              </>

            )}

          </div>

          {assessment && (

            <>
              <div className="practice-result-row">

                <div>
                  <p className="label">Letter</p>
                  <p>{targetLetter}</p>
                </div>

                <div>
                  <p className="label">Prediction</p>
                  <p>
                    {prediction.prediction ??
                      prediction.predicted_sign}
                  </p>
                </div>

                <div>
                  <p className="label">Result</p>

                  <p className={
                    isCorrect
                      ? "result-correct"
                      : "result-incorrect"
                  }>
                    {isCorrect
                      ? "✔️ Correct"
                      : "❌ Incorrect"}
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

              <div className="result-card">
                <ul className="feedback-list">
                  {assessment?.feedback?.length ? (
  assessment.feedback.map((msg, i) => (
    <li key={i}>{msg}</li>
  ))
) : (
  <li>No feedback available.</li>
)}
                </ul>
              </div>

            </>

          )}

        </div>

        <div className="practice-side">

          <div className="reference-card">
            <p className="label">Reference Sign</p>

            <div className="reference-image">
              <span>{targetLetter}</span>
            </div>

            <p className="hint">
              Match your hand shape.
            </p>

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
                {prediction
                  ? ` ${prediction.confidence}%`
                  : " --%"}
              </p>

            </div>

          </div>

        </div>

      </div>
    </div>
  )
}