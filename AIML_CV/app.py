import cv2
import mediapipe as mp

from src.feature_extractor import extract_features
from src.data_collector import save_sample

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

labels = ["A", "B", "C", "L", "Y"]

current_label_index = 0
current_label = labels[current_label_index]

sample_count = 0

cap = cv2.VideoCapture(0)

# Initialize features
features = None

while True:

    success, frame = cap.read()

    if not success:
        print("Failed to capture frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            features = extract_features(hand_landmarks)

    cv2.imshow("Sign Language Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):

        if features is not None:

            save_sample(features, current_label)

            sample_count += 1

            print(f"Saved {current_label} sample #{sample_count}")

        else:

            print("No hand detected! Show your hand before saving.")

    elif key == ord('n'):

        if current_label_index < len(labels) - 1:

            current_label_index += 1
            current_label = labels[current_label_index]
            sample_count = 0

            print(f"\nNow collecting: {current_label}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()