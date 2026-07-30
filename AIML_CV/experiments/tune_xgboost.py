import os
import joblib
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
)

from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier
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
    "best_xgb_tuned.pkl"
)
dataset = pd.read_csv(DATASET_PATH)

X = dataset.drop("label", axis=1)

y = dataset["label"]

encoder = LabelEncoder()

y = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
model = XGBClassifier(

    objective="multi:softmax",

    num_class=len(encoder.classes_),

    eval_metric="mlogloss",

    random_state=42
)
param_grid = {

    "n_estimators": [100, 200, 300],

    "max_depth": [4, 6, 8],

    "learning_rate": [0.05, 0.1],

    "subsample": [0.8, 1.0],

    "colsample_bytree": [0.8, 1.0]

}
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_grid,
    n_iter=15,          # Try only 15 combinations
    cv=5,
    scoring="accuracy",
    random_state=42,
    n_jobs=-1,
    verbose=2
)

random_search.fit(X_train, y_train)
best_model = random_search.best_estimator_

predictions = best_model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nBest Parameters")

print(random_search.best_params_)

print(f"\nAccuracy : {accuracy:.4f}")
joblib.dump(
    best_model,
    MODEL_PATH
)

print("\nBest tuned model saved.")