import os
import time
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from xgboost import XGBClassifier


# ==========================================================
# Load Dataset
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_PATH = os.path.join(
    PROJECT_DIR,
    "dataset",
    "asl_landmarks_final.csv"
)

dataset = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully")
print("Shape:", dataset.shape)


# ==========================================================
# Separate Features and Labels
# ==========================================================

X = dataset.drop("label", axis=1)
y = dataset["label"]


# ==========================================================
# Label Encoding
# ==========================================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

print("\nNumber of Classes:", len(label_encoder.classes_))
print(label_encoder.classes_)


# ==========================================================
# Train-Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================================
# Create XGBoost Model
# ==========================================================

model = XGBClassifier(

    objective="multi:softprob",

    num_class=28,

    n_estimators=200,

    max_depth=6,

    learning_rate=0.1,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    eval_metric="mlogloss"
)


# ==========================================================
# Train Model
# ==========================================================

print("\nTraining XGBoost Model...")

start_time = time.time()

model.fit(X_train, y_train)

training_time = time.time() - start_time


# ==========================================================
# Prediction
# ==========================================================

prediction_start = time.time()

predictions = model.predict(X_test)

prediction_time = time.time() - prediction_start


# ==========================================================
# Accuracy
# ==========================================================

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy : {accuracy*100:.2f}%")

print(f"Training Time : {training_time:.3f} sec")

print(f"Prediction Time : {prediction_time:.3f} sec")


# ==========================================================
# Classification Report
# ==========================================================

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_
    )
)


# ==========================================================
# Save Model
# ==========================================================

MODEL_DIR = os.path.join(PROJECT_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "sign_language_xgb.pkl"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

joblib.dump(model, MODEL_PATH)

joblib.dump(label_encoder, ENCODER_PATH)

print("\nModel Saved Successfully!")

print(MODEL_PATH)

print(ENCODER_PATH)