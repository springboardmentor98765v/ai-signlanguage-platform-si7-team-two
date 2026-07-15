import { useRef, useState, useEffect } from 'react'
import { predictSign, assessAttempt } from '../services/api.js'

// Fallback status label if the backend hasn't sent an `assessment.status`
// field yet — safe to remove once Intern 4's API always returns it.
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
  const [targetLetter] = useState('A')

  const [isChecking, setIsChecking] = useState(false)
  const [checkError, setCheckError] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [assessment, setAssessment] = useState(null)
  const [attemptTime, setAttemptTime] = useState(null)

  useEffect(() => {
    return () => stopStream()
  }, [])

  function stopStream() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
  }

  async function handleStart() {
    setCameraError('')
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      streamRef.current = stream
      if (videoRef.current) videoRef.current.srcObject = stream
      setIsPracticing(true)
    } catch (err) {
      setCameraError('Camera access denied or unavailable. Please allow camera permission and try again.')
      setIsPracticing(false)
    }
  }

  function handleStop() {
    stopStream()
    if (videoRef.current) videoRef.current.srcObject = null
    setIsPracticing(false)
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
      canvas.getContext('2d').drawImage(videoRef.current, 0, 0)
      const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg'))

      // Step 1: no change to this call sequence.
      const predictionResult = await predictSign(blob)
      setPrediction(predictionResult)

      const assessmentResult = await assessAttempt(
        targetLetter,
        predictionResult.predicted_sign,
        predictionResult.confidence
      )
      setAssessment(assessmentResult)

      // Step 4: attempt time, measured on the frontend.
      const elapsedSeconds = ((performance.now() - startedAt) / 1000).toFixed(1)
      setAttemptTime(elapsedSeconds)
    } catch (err) {
      setCheckError(err.message || 'Could not check your sign. Please try again.')
    } finally {
      setIsChecking(false)
    }
  }

  const isCorrect = prediction && prediction.predicted_sign === targetLetter
  const statusLabel = assessment ? (assessment.status || getStatusLabel(assessment.accuracy)) : null

  return (
    <div>
      <div className="practice-header">
        <h2>Practice: Letter {targetLetter}</h2>
        <p className="sub">Show the sign in front of your camera and hold it steady.</p>
      </div>

      <div className="practice-grid">
        <div className="practice-panel">
          <div className="video-frame">
            {isPracticing ? (
              <video ref={videoRef} autoPlay playsInline muted className="video-feed" />
            ) : (
              <div className="video-placeholder"><span>Camera is off</span></div>
            )}
          </div>
          <canvas ref={canvasRef} style={{ display: 'none' }} />

          {cameraError && <p className="camera-error">{cameraError}</p>}
          {checkError && <p className="camera-error">{checkError}</p>}

          <div className="practice-controls">
            {!isPracticing ? (
              <button className="btn-primary" onClick={handleStart}>Start Practice</button>
            ) : (
              <>
                <button className="btn-stop" onClick={handleStop}>Stop Practice</button>
                <button className="btn-check" onClick={handleCheckSign} disabled={isChecking}>
                  {isChecking ? 'Checking...' : 'Check My Sign'}
                </button>
              </>
            )}
          </div>

          {assessment && (
            <>
              {/* Step 5: practice result row */}
              <div className="practice-result-row">
                <div>
                  <p className="label">Letter</p>
                  <p className="result-value">{targetLetter}</p>
                </div>
                <div>
                  <p className="label">Prediction</p>
                  <p className="result-value">{prediction.predicted_sign}</p>
                </div>
                <div>
                  <p className="label">Result</p>
                  <p className={`result-value ${isCorrect ? 'result-correct' : 'result-incorrect'}`}>
                    {isCorrect ? '✔️ Correct' : '❌ Incorrect'}
                  </p>
                </div>
              </div>

              {/* Step 2: assessment summary card */}
              <div className="summary-card">
                <p className="label">Assessment Summary</p>

                <div className="summary-row">
                  <span>Prediction</span>
                  <span>{prediction.predicted_sign}</span>
                </div>

                <div className="summary-row">
                  <span>Confidence</span>
                  <span>{prediction.confidence}%</span>
                </div>
                <div className="accuracy-bar-wrap">
                  <div
                    className={`accuracy-bar ${prediction.confidence < 70 ? 'low' : ''}`}
                    style={{ width: `${prediction.confidence}%` }}
                  />
                  <span>{prediction.confidence}%</span>
                </div>

                <div className="summary-row">
                  <span>Accuracy</span>
                  <span>{assessment.accuracy}%</span>
                </div>
                <div className="accuracy-bar-wrap">
                  <div
                    className={`accuracy-bar ${assessment.accuracy < 70 ? 'low' : ''}`}
                    style={{ width: `${assessment.accuracy}%` }}
                  />
                  <span>{assessment.accuracy}%</span>
                </div>

                <div className="summary-row">
                  <span>Status</span>
                  <span className={`status-badge ${assessment.accuracy < 70 ? 'low' : ''}`}>{statusLabel}</span>
                </div>

                {attemptTime && (
                  <div className="summary-row">
                    <span>Attempt Time</span>
                    <span>{attemptTime} seconds</span>
                  </div>
                )}
              </div>

              {/* Step 3: checklist-style feedback */}
              <div className="result-card">
                <ul className="feedback-list checklist">
                  {assessment.feedback.map((msg, i) => (
                    <li key={i}>{msg}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>

        <div className="practice-side">
          <div className="reference-card">
            <p className="label">Reference Sign</p>
            <div className="reference-image"><span>{targetLetter}</span></div>
            <p className="hint">Match your hand shape to this reference.</p>
          </div>

          <div className="prediction-card">
            <p className="label">AI Prediction</p>
            <div className="prediction-placeholder">
              <p className="predicted-sign">{prediction ? prediction.predicted_sign : '--'}</p>
              <p className="confidence">
                Confidence: {prediction ? `${prediction.confidence}%` : '--%'}
              </p>
            </div>
            <p className="hint">Prediction updates each time you click "Check My Sign".</p>
          </div>
        </div>
      </div>
    </div>
  )
}
