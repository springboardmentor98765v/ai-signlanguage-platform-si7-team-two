"""
Application Configuration
"""

# -------------------------
# Model Configuration
# -------------------------

MODEL_PATH = "models/best_xgb_tuned.pkl"
LABEL_ENCODER_PATH = "models/label_encoder.pkl"

# -------------------------
# MediaPipe Configuration
# -------------------------

MAX_NUM_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# -------------------------
# Prediction Configuration
# -------------------------

CONFIDENCE_THRESHOLD = 0.80

TEMPORAL_SMOOTHING_WINDOW = 5

# -------------------------
# Webcam Configuration
# -------------------------

CAMERA_INDEX = 0

WINDOW_NAME = "Sign Language Assessment"