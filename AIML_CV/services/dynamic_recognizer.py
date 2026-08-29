import numpy as np
from collections import deque

from src.dynamic_feature_extractor import extract_dynamic_features
from inference.dynamic_predictor import predict_dynamic_sign


class DynamicSignRecognizer:

    # ============================================================
    # CONFIGURATION
    # ============================================================

    SEQUENCE_LENGTH = 25

    def __init__(self):

        # Stores the latest 25 feature frames
        self.sequence = deque(
            maxlen=self.SEQUENCE_LENGTH
        )

    # ============================================================
    # RESET SEQUENCE
    # ============================================================

    def reset(self):

        """
        Clear the current sequence.
        """

        self.sequence.clear()

    # ============================================================
    # ADD FRAME
    # ============================================================

    def add_frame(self, holistic_results):

        """
        Extract features from one MediaPipe Holistic frame
        and add them to the current sequence.
        """

        features = extract_dynamic_features(
            holistic_results
        )

        # Safety validation
        if features.shape != (285,):

            raise ValueError(
                f"Expected feature shape (285,), "
                f"but received {features.shape}"
            )

        self.sequence.append(features)

        return len(self.sequence)

    # ============================================================
    # CHECK SEQUENCE
    # ============================================================

    def is_ready(self):

        """
        Return True when 25 frames are collected.
        """

        return len(self.sequence) == self.SEQUENCE_LENGTH

    # ============================================================
    # PREDICT
    # ============================================================

    def predict(self):

        """
        Predict the dynamic sign when 25 frames
        are available.
        """

        if not self.is_ready():

            return {
                "ready": False,
                "frames_collected": len(self.sequence),
                "frames_required": self.SEQUENCE_LENGTH,
                "prediction": None,
                "confidence": 0.0
            }

        # Convert deque → NumPy array
        input_sequence = np.array(
            self.sequence,
            dtype=np.float32
        )

        # Shape validation
        if input_sequence.shape != (25, 285):

            raise ValueError(
                f"Expected sequence shape (25, 285), "
                f"but received {input_sequence.shape}"
            )

        # Run LSTM prediction
        result = predict_dynamic_sign(
            input_sequence
        )

        return {
            "ready": True,
            "frames_collected": self.SEQUENCE_LENGTH,
            "frames_required": self.SEQUENCE_LENGTH,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"]
        }