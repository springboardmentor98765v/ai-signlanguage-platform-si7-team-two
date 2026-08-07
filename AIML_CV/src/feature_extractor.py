import numpy as np

def extract_features(hand_landmarks):

    wrist = hand_landmarks.landmark[0]

    features = []

    for lm in hand_landmarks.landmark:

        features.extend([
            lm.x - wrist.x,
            lm.y - wrist.y,
            lm.z - wrist.z
        ])

    # Wrist becomes origin
    features[0] = 0.0
    features[1] = 0.0
    features[2] = 0.0

    return np.array(features, dtype=np.float32)