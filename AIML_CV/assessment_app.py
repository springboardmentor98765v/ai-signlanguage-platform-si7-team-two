import cv2
import mediapipe as mp
from collections import deque, Counter

from src.feature_extractor import extract_features
from inference.predictor import predict_sign
from assessment.assessment_engine import AssessmentEngine
from assessment.score_manager import ScoreManager
from config.settings import CONFIDENCE_THRESHOLD
# -----------------------------
# MediaPipe Initialization
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# Assessment
# -----------------------------
assessment = AssessmentEngine()
score_manager = ScoreManager()

current_target = assessment.current_letter

status = "Waiting..."
prediction = "No Hand"
smoothed_prediction = "No Hand"
confidence = 0.0

prediction_history = deque(maxlen=5)
question_answered = False

correct = 0
total = 0

# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    prediction = "No Hand"
    confidence = 0.0

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            features = extract_features(hand_landmarks)

            prediction, confidence = predict_sign(features)

            if confidence >= CONFIDENCE_THRESHOLD and prediction != "Unknown":
                prediction_history.append(prediction)

            if prediction_history:
                smoothed_prediction = Counter(prediction_history).most_common(1)[0][0]
            else:
                smoothed_prediction = "Unknown"

            prediction = smoothed_prediction

    # -----------------------------
    # Status Color
    # -----------------------------
    if status == "Correct":
        status_color = (0, 255, 0)
    elif status == "Incorrect":
        status_color = (0, 0, 255)
    else:
        status_color = (0, 255, 255)

    accuracy = score_manager.get_accuracy()

    # -----------------------------
    # UI
    # -----------------------------
    cv2.putText(frame, f"Target : {current_target}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.putText(frame, f"Prediction : {prediction}", (20,80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"Confidence : {confidence*100:.2f}%", (20,120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.putText(frame, f"Status : {status}", (20,160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

    cv2.putText(frame, f"Score : {correct}/{total}", (20,200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    cv2.putText(frame, f"Accuracy : {accuracy:.2f}%", (20,240),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

    cv2.putText(frame, "SPACE - Submit", (20,280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, "N - Next Question", (20,310),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, "Q - Quit", (20,340),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Sign Language Assessment", frame)

    key = cv2.waitKey(1) & 0xFF

    # -----------------------------
    # Submit Answer
    # -----------------------------
    if key == ord(" "):

        if not question_answered:

            if prediction == "Unknown" or prediction == "No Hand":
                status = "Show a valid sign"

            else:
                is_correct = assessment.evaluate(prediction)

                score_manager.update(is_correct)

                correct, total = score_manager.get_score()

                if is_correct:
                    status = "Correct"
                else:
                    status = "Incorrect"

                question_answered = True

    # -----------------------------
    # Next Question
    # -----------------------------
    elif key == ord("n"):

        current_target = assessment.next_question()

        status = "Waiting..."

        question_answered = False

        prediction_history.clear()

        prediction = "No Hand"
        smoothed_prediction = "No Hand"
        confidence = 0.0

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()