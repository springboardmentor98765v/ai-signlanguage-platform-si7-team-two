import os
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


# ==========================================================
# Paths
# ==========================================================

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

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "evaluation",
    "results"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# Load Dataset
# ==========================================================

dataset = pd.read_csv(DATASET_PATH)

X = dataset.drop("label", axis=1)
y = dataset["label"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Dataset Loaded")

# ==========================================================
# Load Model
# ==========================================================

model = joblib.load(MODEL_PATH)

print("Model Loaded")

# ==========================================================
# Prediction
# ==========================================================

predictions = model.predict(X_test)

# ==========================================================
# Accuracy
# ==========================================================

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy*100:.2f}%")

# ==========================================================
# Classification Report
# ==========================================================

report = classification_report(
    y_test,
    predictions,
    target_names=label_encoder.classes_,
)

print(report)

with open(
    os.path.join(OUTPUT_DIR, "classification_report.txt"),
    "w"
) as f:

    f.write(report)

# ==========================================================
# Metrics JSON
# ==========================================================

metrics = {
    "accuracy": float(accuracy)
}

with open(
    os.path.join(OUTPUT_DIR, "metrics.json"),
    "w"
) as f:

    json.dump(metrics, f, indent=4)

# ==========================================================
# Predictions CSV
# ==========================================================

prediction_df = pd.DataFrame({

    "Actual":
        label_encoder.inverse_transform(y_test),

    "Predicted":
        label_encoder.inverse_transform(predictions)

})

prediction_df.to_csv(

    os.path.join(
        OUTPUT_DIR,
        "predictions.csv"
    ),

    index=False

)

# ==========================================================
# Confusion Matrix
# ==========================================================

cm = confusion_matrix(
    y_test,
    predictions
)

cm_df = pd.DataFrame(
    cm,
    index=label_encoder.classes_,
    columns=label_encoder.classes_
)

cm_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "confusion_matrix.csv"
    )
)

plt.figure(figsize=(14,12))

sns.heatmap(
    cm_df,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "confusion_matrix.png"
    )
)

plt.close()

print("\nEvaluation Completed Successfully")

print("\nSaved to:")

print(OUTPUT_DIR)