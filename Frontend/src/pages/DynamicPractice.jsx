import {
  useRef,
  useState,
  useEffect,
} from "react";

import {
  useParams,
  useNavigate,
} from "react-router-dom";

import {
  predictDynamicSign,
  startPracticeSession,
  endPracticeSession,
  getLessons,
} from "../services/api.js";

import { getUser } from "../utils/auth.js";


export default function DynamicPractice() {
  const { word } = useParams();

  const targetWord = decodeURIComponent(word || "");

  const navigate = useNavigate();

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);
  const sessionIdRef = useRef(null);

  const [isPracticing, setIsPracticing] =
    useState(false);

  const [cameraError, setCameraError] =
    useState("");

  const [checkError, setCheckError] =
    useState("");

  const [isChecking, setIsChecking] =
    useState(false);

  const [prediction, setPrediction] =
    useState(null);

  const [sessionId, setSessionId] =
    useState(null);

  const [lessons, setLessons] =
    useState([]);


  useEffect(() => {
    async function loadLessons() {
      try {
        const data = await getLessons();
        setLessons(data);
      } catch (error) {
        console.error(
          "Failed to load lessons",
          error
        );
      }
    }

    loadLessons();
  }, []);


  useEffect(() => {
    if (
      isPracticing &&
      videoRef.current &&
      streamRef.current
    ) {
      videoRef.current.srcObject =
        streamRef.current;
    }
  }, [isPracticing]);


  useEffect(() => {
    return () => {
      stopStream();

      if (sessionIdRef.current) {
        endPracticeSession(
          sessionIdRef.current
        ).catch(() => {});
      }
    };
  }, []);


  function stopStream() {
    if (!streamRef.current) return;

    streamRef.current
      .getTracks()
      .forEach((track) => track.stop());

    streamRef.current = null;
  }


  async function handleStart() {
    setCameraError("");
    setCheckError("");
    setPrediction(null);

    try {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: {
            width: 640,
            height: 480,
            facingMode: "user",
          },
          audio: false,
        });

      streamRef.current = stream;

      setIsPracticing(true);


      // Create practice session
      try {
        const user = getUser();

        /*
        We need a valid lesson_id because your
        practice_sessions table requires lesson_id.

        For now, use the first available lesson.
        Later we can create proper Word Lessons
        in the database.
        */

        const lesson = lessons[0];

        if (user?.id && lesson?.id) {
          const session =
            await startPracticeSession(
              user.id,
              lesson.id
            );

          setSessionId(
            session.session_id
          );

          sessionIdRef.current =
            session.session_id;
        }
      } catch (error) {
        console.error(
          "Could not create practice session:",
          error
        );
      }

    } catch (error) {
      console.error(error);

      setCameraError(
        "Camera access denied or unavailable. Please allow camera permission."
      );

      setIsPracticing(false);
    }
  }


  async function handleStop() {
    stopStream();

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsPracticing(false);


    if (sessionIdRef.current) {
      try {
        await endPracticeSession(
          sessionIdRef.current
        );
      } catch (error) {
        console.error(
          "Failed to end practice session:",
          error
        );
      }

      setSessionId(null);
      sessionIdRef.current = null;
    }
  }


  async function handleCheckWord() {
    if (!videoRef.current) return;

    const user = getUser();

    if (!user?.id) {
      setCheckError(
        "User information not found. Please login again."
      );

      return;
    }

    if (!sessionIdRef.current) {
      setCheckError(
        "Practice session is not ready yet."
      );

      return;
    }


    setIsChecking(true);

    setCheckError("");

    setPrediction(null);


    try {
      const canvas =
        canvasRef.current;

      canvas.width =
        videoRef.current.videoWidth;

      canvas.height =
        videoRef.current.videoHeight;


      canvas
        .getContext("2d")
        .drawImage(
          videoRef.current,
          0,
          0
        );


      const blob =
        await new Promise(
          (resolve) =>
            canvas.toBlob(
              resolve,
              "image/jpeg"
            )
        );


      if (!blob) {
        throw new Error(
          "Unable to capture webcam frame."
        );
      }


      const result =
        await predictDynamicSign(
          blob,
          user.id,
          sessionIdRef.current,
          targetWord
        );


      /*
      Dynamic AI model may return:

      {
        ready: true,
        prediction: "Good",
        confidence: 76.41,
        is_correct: true
      }

      OR while collecting frames:

      {
        ready: false,
        frames_collected: 10,
        frames_required: 25
      }
      */

      setPrediction(result);

    } catch (error) {
      console.error(error);

      setCheckError(
        error.message ||
        "Could not check your word sign."
      );
    } finally {
      setIsChecking(false);
    }
  }


  const isCorrect =
    prediction?.is_correct === true;


  return (
    <div>

      <div className="practice-header">

        <div>

          <button
            className="btn-secondary"
            onClick={() =>
              navigate("/word-lessons")
            }
          >
            ← Back to Words
          </button>


          <h2>
            Practice Word: {targetWord}
          </h2>


          <p className="sub">
            Perform the complete sign for the word
            and let the AI analyze your movement.
          </p>

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

              <div className="video-placeholder">
                Camera is Off
              </div>

            )}

          </div>


          <canvas
            ref={canvasRef}
            style={{
              display: "none",
            }}
          />


          {cameraError && (

            <p
              className="camera-error"
              role="alert"
            >
              {cameraError}
            </p>

          )}


          {checkError && (

            <p
              className="camera-error"
              role="alert"
            >
              {checkError}
            </p>

          )}


          <div className="practice-controls">

            {!isPracticing ? (

              <button
                className="btn-primary"
                onClick={handleStart}
              >
                Start Word Practice
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
                  onClick={handleCheckWord}
                  disabled={isChecking}
                >
                  {isChecking
                    ? "Checking..."
                    : "Check My Word"}
                </button>

              </>

            )}

          </div>


          {prediction && (

            <div
              className="result-card"
              style={{
                marginTop: "20px",
              }}
            >

              {!prediction.ready ? (

                <>

                  <h3>
                    Collecting Movement Frames
                  </h3>

                  <p>
                    Frames collected:
                    {" "}
                    {prediction.frames_collected}
                    {" / "}
                    {prediction.frames_required}
                  </p>

                  <p>
                    Keep performing the sign.
                  </p>

                </>

              ) : (

                <>

                  <h3>
                    Prediction Result
                  </h3>


                  <div className="practice-result-row">

                    <div>

                      <p className="label">
                        Expected Word
                      </p>

                      <p>
                        {targetWord}
                      </p>

                    </div>


                    <div>

                      <p className="label">
                        AI Prediction
                      </p>

                      <p>
                        {prediction.prediction}
                      </p>

                    </div>


                    <div>

                      <p className="label">
                        Result
                      </p>

                      <p
                        className={
                          isCorrect
                            ? "result-correct"
                            : "result-incorrect"
                        }
                      >
                        {isCorrect
                          ? "✔ Correct"
                          : "✖ Incorrect"}
                      </p>

                    </div>

                  </div>


                  <div className="summary-card">

                    <div className="summary-row">

                      <span>
                        Confidence
                      </span>

                      <span>
                        {prediction.confidence}%
                      </span>

                    </div>


                    <div className="summary-row">

                      <span>
                        Frames
                      </span>

                      <span>
                        {prediction.frames_collected}
                        {" / "}
                        {prediction.frames_required}
                      </span>

                    </div>

                  </div>

                </>

              )}

            </div>

          )}

        </div>


        <div className="practice-side">

          <div className="reference-card">

            <p className="label">
              Target Word
            </p>


            <div className="reference-image">

              <span>
                {targetWord}
              </span>

            </div>


            <p className="hint">
              Perform the complete sign naturally.
            </p>

          </div>


          <div className="prediction-card">

            <p className="label">
              Dynamic AI Prediction
            </p>


            <div className="prediction-placeholder">

              <p className="predicted-sign">

                {prediction?.prediction || "--"}

              </p>


              <p className="confidence">

                Confidence:

                {prediction?.confidence
                  ? ` ${prediction.confidence}%`
                  : " --%"}

              </p>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}