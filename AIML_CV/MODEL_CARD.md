# Model Card — Sign Language Recognition (XGBoost + MediaPipe)

**Owner:** Intern 3 (AI/ML & CV)
**Milestone:** 1
**Last Updated:** July 2026

---

## Model Overview

| Field | Value |
|---|---|
| **Model Type** | XGBoost Classifier (`xgboost==3.2.0`) |
| **Task** | Multi-class classification of ASL hand signs (A–Z) |
| **Input** | 63 normalized landmark features extracted from a single hand |
| **Output** | Predicted sign label + confidence probability |
| **Model File** | `models/sign_language_xgb.pkl` (~5.5 MB) |
| **Encoder File** | `models/label_encoder.pkl` (~590 bytes) |
| **Confidence Threshold** | 0.80 — predictions below this are returned as `"Unknown"` |

---

## Feature Extraction

Features are extracted via **MediaPipe Hands** landmark detection:

- 21 hand landmarks × (x, y, z) coordinates = **63 features**
- Extracted by `src/feature_extractor.py` via `extract_features(hand_landmarks)`
- MediaPipe config: `max_num_hands=1`, `min_detection_confidence=0.5`, `min_tracking_confidence=0.5`

---

## Inference Pipeline

```
Webcam frame (BGR)
    ↓  cv2.cvtColor → RGB
    ↓  mediapipe.Hands.process()
    ↓  extract_features(hand_landmarks)  → float[63]
    ↓  XGBoost.predict_proba()
    ↓  label_encoder.inverse_transform()
    → (sign_label: str, confidence: float)
```

Entry points:
- **REST API:** `api/main.py` → `POST /predict` (accepts image upload)
- **Live Assessment:** `assessment_app.py` (webcam loop with prediction smoothing)
- **Direct inference:** `inference/predictor.py::predict_sign(features)`

---

## Response Schema

The `/predict` API endpoint returns:

```json
{
  "prediction": "A",
  "confidence": 95.42
}
```

This matches the contract consumed by Intern 4's Assessment Service (`predicted_sign`, `confidence` as percentage).

> **Note on Intern 5's DB contract:** The `assessments` table stores `predicted_sign` (VARCHAR) and `confidence` (NUMERIC). The API returns confidence as a percentage (`confidence * 100`, rounded to 2dp), which is what gets stored.

---

## Feedback Category Mapping

When the model's `possible_issue` output indicates finger-level errors (e.g., incorrect curl or extension), these are mapped to the `hand_shape` feedback category in the assessment layer. This is consistent with the DB constraint in `Database_Devops/db/models/feedback.py`.

| AI Issue Type | DB Feedback Category |
|---|---|
| hand orientation | `hand_shape` |
| finger position / curl | `hand_shape` (mapped — see TODO in feedback.py) |
| sign timing / hold duration | `timing` |
| hand position in frame | `position` |
| movement trajectory | `motion` |

---

## Known Limitations

- Trained on static images; real-time performance depends on lighting and background
- `"Unknown"` returned for low-confidence predictions (< 0.80) — this is intentional to avoid noisy feedback
- Currently supports single-hand detection only (`max_num_hands=1`)
- Model covers the ASL alphabet (A–Z static signs); dynamic signs (J, Z) may have reduced accuracy

---

## Dataset

See `ROBUSTNESS_TESTING.md` for test performance breakdown.
Training dataset: `dataset/` directory (not committed — contact Intern 3 for access).
