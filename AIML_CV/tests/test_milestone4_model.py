import os
import time
import joblib
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_xgb_tuned.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoder.pkl"
)


def main():

    print("=" * 60)
    print("MILESTONE 4 - AI MODEL VALIDATION")
    print("=" * 60)

    # --------------------------------------------------
    # Check files
    # --------------------------------------------------

    assert os.path.exists(MODEL_PATH), \
        "Model file not found!"

    assert os.path.exists(ENCODER_PATH), \
        "Label encoder not found!"

    print("\n✓ Model file found")
    print("✓ Label encoder found")

    # --------------------------------------------------
    # Load model
    # --------------------------------------------------

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)

    print("\n✓ Model loaded successfully")
    print("✓ Encoder loaded successfully")

    # --------------------------------------------------
    # Check classes
    # --------------------------------------------------

    classes = encoder.classes_

    print("\nNumber of classes:", len(classes))

    print("Classes:")
    print(list(classes))

    assert len(classes) == 28, \
        "Expected exactly 28 classes!"

    print("✓ 28 classes confirmed")

    # --------------------------------------------------
    # Check feature count
    # --------------------------------------------------

    print("\nExpected features:", model.n_features_in_)

    assert model.n_features_in_ == 63, \
        "Expected 63 input features!"

    print("✓ 63 input features confirmed")

    # --------------------------------------------------
    # Dummy prediction
    # --------------------------------------------------

    features = np.zeros((1, 63), dtype=np.float32)

    start = time.perf_counter()

    prediction = model.predict(features)

    probabilities = model.predict_proba(features)

    elapsed = time.perf_counter() - start

    predicted_class = encoder.inverse_transform(prediction)[0]

    confidence = float(np.max(probabilities[0])) * 100

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    print("\nPrediction:", predicted_class)

    print(
        f"Confidence: {confidence:.2f}%"
    )

    print(
        f"Prediction Time: {elapsed:.4f} sec"
    )

    assert predicted_class in classes, \
        "Prediction is not a known class!"

    print("✓ Prediction belongs to known classes")

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("MODEL VALIDATION PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()