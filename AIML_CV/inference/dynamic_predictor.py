from pathlib import Path
import pickle

import numpy as np
import tensorflow as tf


# ==========================================================
# PATH CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "dynamic_sign_model.keras"

ENCODER_PATH = BASE_DIR / "models" / "dynamic_label_encoder.pkl"


# ==========================================================
# LOAD MODEL
# ==========================================================

print("Loading Dynamic Sign Language Model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Dynamic model loaded successfully!")


# ==========================================================
# LOAD LABEL ENCODER
# ==========================================================

print("Loading Dynamic Label Encoder...")

with open(ENCODER_PATH, "rb") as file:
    label_encoder = pickle.load(file)

print("Dynamic label encoder loaded successfully!")


# ==========================================================
# PREDICTION FUNCTION
# ==========================================================

def predict_dynamic_sign(sequence):

    """
    Predict a dynamic ASL word.

    Expected input:
        sequence shape = (25, 285)
    """

    sequence = np.array(sequence, dtype=np.float32)

    # Validate shape
    if sequence.shape != (25, 285):
        raise ValueError(
            f"Expected sequence shape (25, 285), "
            f"but received {sequence.shape}"
        )

    # Add batch dimension
    sequence = np.expand_dims(sequence, axis=0)

    # Model prediction
    probabilities = model.predict(
        sequence,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        np.max(probabilities) * 100
    )

    # Convert predicted index to word
    predicted_label = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    return {
        "prediction": predicted_label,
        "confidence": round(confidence, 2),
        "probabilities": probabilities.tolist()
    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("DYNAMIC MODEL TEST")
    print("=" * 60)

    dummy_sequence = np.zeros(
        (25, 285),
        dtype=np.float32
    )

    result = predict_dynamic_sign(
        dummy_sequence
    )

    print("\nPrediction:")
    print(result["prediction"])

    print("\nConfidence:")
    print(result["confidence"])

    print("\nPrediction successful!")