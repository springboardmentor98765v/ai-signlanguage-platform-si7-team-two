import numpy as np

def extract_features(hand_landmarks):

    features = []

    for landmark in hand_landmarks.landmark:
        features.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    return np.array(features)