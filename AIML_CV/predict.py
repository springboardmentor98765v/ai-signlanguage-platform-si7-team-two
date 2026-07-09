import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sign_language_rf.pkl"
)

model = joblib.load(MODEL_PATH)

print("Random Forest model loaded successfully!")