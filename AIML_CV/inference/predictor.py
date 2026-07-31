import os
import joblib

# -------------------------------------------------
# Load Model
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "best_xgb_tuned.pkl"
)



ENCODER_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "label_encoder.pkl"
)

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

print("✅ XGBoost model loaded successfully!")
print("✅ Label Encoder loaded successfully!")
import numpy as np

def predict_sign(features):

    features = np.array(features).reshape(1, -1)

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    confidence = round(float(np.max(probabilities) * 100), 2)

    label = label_encoder.inverse_transform([prediction])[0]

    THRESHOLD = 80.0

    if confidence < THRESHOLD:
        label = "Unknown"

    return label, confidence
if __name__ == "__main__":

    dummy_features = [0.0] * 63

    prediction = predict_sign(dummy_features)

    print("Prediction:", prediction)
    print("Loaded model from:", MODEL_PATH)