import os
import json
import time
import joblib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "asl_landmarks_final.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "sign_language_xgb.pkl"
)

ENCODER_PATH = os.path.join(
    PROJECT_DIR,
    "models",
    "label_encoder.pkl"
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "evaluation",
    "results"
)

os.makedirs(RESULTS_DIR, exist_ok=True)
def load_dataset():

    dataset = pd.read_csv(DATASET_PATH)

    X = dataset.drop("label", axis=1)

    y = dataset["label"]

    return X, y
def load_model():

    model = joblib.load(MODEL_PATH)

    encoder = joblib.load(ENCODER_PATH)

    return model, encoder
def evaluate_model(model, encoder, X, y):

    y_encoded = encoder.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.20,
        random_state=42,
        stratify=y_encoded
    )

    start_time = time.time()

    predictions = model.predict(X_test)

    prediction_time = time.time() - start_time

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions,
        target_names=encoder.classes_,
        output_dict=True
    )

    cm = confusion_matrix(
        y_test,
        predictions
    )

    return (
        accuracy,
        report,
        cm,
        prediction_time,
        y_test,
        predictions
    )
def save_classification_report(
    y_test,
    predictions,
    encoder
):
    """
    Save the classification report as a text file.
    """

    report_text = classification_report(
        y_test,
        predictions,
        target_names=encoder.classes_
    )

    report_path = os.path.join(
        RESULTS_DIR,
        "classification_report.txt"
    )

    with open(report_path, "w") as f:
        f.write(report_text)

    print("✓ Classification Report Saved")
def save_confusion_matrix_csv(cm, encoder):

    cm_df = pd.DataFrame(
        cm,
        index=encoder.classes_,
        columns=encoder.classes_
    )

    cm_path = os.path.join(
        RESULTS_DIR,
        "confusion_matrix.csv"
    )

    cm_df.to_csv(cm_path)

    print("✓ Confusion Matrix CSV Saved")
def save_confusion_matrix_png(cm, encoder):
    """
    Save the confusion matrix as an image.
    """

    plt.figure(figsize=(14, 12))

    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)

    plt.title("Confusion Matrix")

    plt.colorbar()

    tick_marks = np.arange(len(encoder.classes_))

    plt.xticks(
        tick_marks,
        encoder.classes_,
        rotation=90
    )

    plt.yticks(
        tick_marks,
        encoder.classes_
    )

    plt.xlabel("Predicted Label")

    plt.ylabel("True Label")

    plt.tight_layout()

    image_path = os.path.join(
        RESULTS_DIR,
        "confusion_matrix.png"
    )

    plt.savefig(
        image_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("✓ Confusion Matrix Image Saved")
def identify_weak_letters(report):
    """
    Identify letters with F1-score below 0.80.
    """

    weak_letters = []

    for label, values in report.items():

        if label in [
            "accuracy",
            "macro avg",
            "weighted avg"
        ]:
            continue

        f1 = values["f1-score"]

        if f1 < 0.80:

            weak_letters.append({

                "Letter": label,

                "Precision": round(values["precision"], 3),

                "Recall": round(values["recall"], 3),

                "F1-Score": round(f1, 3),

                "Support": int(values["support"])

            })

    weak_df = pd.DataFrame(weak_letters)

    weak_path = os.path.join(
        RESULTS_DIR,
        "weak_letters.csv"
    )

    weak_df.to_csv(
        weak_path,
        index=False
    )

    print("✓ Weak Letter Report Saved")

    return weak_df
def save_metrics(
    accuracy,
    prediction_time,
    report
):
    """
    Save evaluation metrics as JSON.
    """

    metrics = {

        "accuracy": round(float(accuracy), 4),

        "prediction_time_seconds": round(
            prediction_time,
            4
        ),

        "macro_precision":
            round(report["macro avg"]["precision"], 4),

        "macro_recall":
            round(report["macro avg"]["recall"], 4),

        "macro_f1":
            round(report["macro avg"]["f1-score"], 4),

        "weighted_precision":
            round(report["weighted avg"]["precision"], 4),

        "weighted_recall":
            round(report["weighted avg"]["recall"], 4),

        "weighted_f1":
            round(report["weighted avg"]["f1-score"], 4)

    }

    json_path = os.path.join(
        RESULTS_DIR,
        "metrics.json"
    )

    with open(
        json_path,
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print("✓ Metrics JSON Saved")
def save_predictions(
    y_test,
    predictions,
    encoder
):

    actual = encoder.inverse_transform(y_test)

    predicted = encoder.inverse_transform(predictions)

    df = pd.DataFrame({

        "Actual": actual,

        "Predicted": predicted

    })

    prediction_path = os.path.join(
        RESULTS_DIR,
        "predictions.csv"
    )

    df.to_csv(
        prediction_path,
        index=False
    )

    print("✓ Predictions Saved")
def print_summary(
    accuracy,
    prediction_time,
    weak_df
):
    """
    Print evaluation summary.
    """

    print("\n" + "=" * 60)

    print("MODEL EVALUATION SUMMARY")

    print("=" * 60)

    print(f"Accuracy            : {accuracy*100:.2f}%")

    print(f"Prediction Time     : {prediction_time:.4f} sec")

    print(f"Weak Letters Found  : {len(weak_df)}")

    if len(weak_df) > 0:

        print("\nLetters Needing Improvement:")

        for letter in weak_df["Letter"]:

            print(f"  • {letter}")

    else:

        print("\nExcellent! No weak letters detected.")

    print("=" * 60)
def main():

    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    X, y = load_dataset()

    model, encoder = load_model()

    (
        accuracy,
        report,
        cm,
        prediction_time,
        y_test,
        predictions
    ) = evaluate_model(
        model,
        encoder,
        X,
        y
    )
    save_classification_report(
    y_test,
    predictions,
    encoder
  )

    save_confusion_matrix_csv(
        cm,
        encoder
    )

    save_confusion_matrix_png(
        cm,
        encoder
    )

    save_predictions(
        y_test,
        predictions,
        encoder
    )

    weak_df = identify_weak_letters(
        report
    )

    save_metrics(
        accuracy,
        prediction_time,
        report
    )

    print_summary(
        accuracy,
        prediction_time,
        weak_df
    )
    print(f"\nAccuracy : {accuracy*100:.2f}%")

    print(
        f"Prediction Time : {prediction_time:.4f} sec"
    )

if __name__ == "__main__":
    main()
