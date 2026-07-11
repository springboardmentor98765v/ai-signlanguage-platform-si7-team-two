import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "asl_landmarks_final.csv"
)

dataset = pd.read_csv(DATASET_PATH)

X = dataset.drop("label", axis=1)

y = dataset["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
models = {
    "KNN": KNeighborsClassifier(n_neighbors=3),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "SVM": SVC()
}
results = {}

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    results[name] = accuracy

    print(f"{name} Accuracy: {accuracy * 100:.2f}%")
print("\n========== Model Comparison ==========")

for name, accuracy in results.items():
    print(f"{name}: {accuracy * 100:.2f}%")
best_model_name = max(results, key=results.get)

print(f"\nBest Model: {best_model_name}")
print(f"Best Accuracy: {results[best_model_name] * 100:.2f}%")
best_model = models[best_model_name]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "sign_language_rf.pkl")

joblib.dump(best_model, MODEL_PATH)

print(f"\nBest model saved successfully at:\n{MODEL_PATH}")