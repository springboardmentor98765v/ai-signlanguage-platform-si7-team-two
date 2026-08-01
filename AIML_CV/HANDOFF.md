# AI/CV Module Handoff

## Service

FastAPI AI Service

Default Port:

8001

---

## Endpoint

POST /predict

Input:

Multipart image

Output:

```json
{
    "prediction": "A",
    "confidence": 97.30,
    "possible_issue": "Excellent! Your sign looks correct."
}
```

---

## Model Files

models/sign_language_xgb.pkl

models/label_encoder.pkl

---

## Documents

MODEL_CARD.md

ROBUSTNESS_TESTING.md

---

## Notes

Supports:

- A-Z
- del
- space

Total Classes:

28

Uses:

- MediaPipe
- XGBoost
