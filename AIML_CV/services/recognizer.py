import mediapipe as mp

from src.feature_extractor import extract_features
from inference.predictor import predict_sign

from config.settings import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE
)


class SignLanguageRecognizer:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )

    def detect_hand(self, rgb_frame):

        return self.hands.process(rgb_frame)

    def extract(self, hand_landmarks):

        return extract_features(hand_landmarks)

    def classify(self, features):

        return predict_sign(features)

    def predict(self, rgb_frame):

        results = self.detect_hand(rgb_frame)

        if not results.multi_hand_landmarks:
            return {
                "prediction": "No Hand",
                "confidence": 0.0,
                "features": None,
                "landmarks": None
            }

        hand = results.multi_hand_landmarks[0]

        features = self.extract(hand)

        prediction, confidence = self.classify(features)

        return {
        "prediction": prediction,
        "confidence": confidence,
        "features": features,
        "landmarks": hand
        }