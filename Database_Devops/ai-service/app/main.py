"""
ai-service/app/main.py

PLACEHOLDER AI/CV service. Intern 3 owns the real MediaPipe hand-landmark
detection + gesture classification (SRS §6, Intern 3, FR-3) — this stub
exists only so Day 5's Docker Compose stack has a real container to build,
run, and health-check against, and so Day 7's integration test can exercise
the exact response shape the real service will eventually return.

`/predict` here does NOT do any real computer vision — it always returns a
fixed, clearly-fake prediction. Replace this endpoint's body with the real
MediaPipe + classifier pipeline; keep the response shape
({"predicted_sign": ..., "confidence": ...}) since Intern 4's Assessment
Service (Day 4) is built to consume exactly that shape.
"""
from fastapi import FastAPI

app = FastAPI(title="Sign Language Platform — AI/CV Service (PLACEHOLDER)")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-service", "note": "placeholder service — Intern 3's real MediaPipe pipeline replaces this"}


@app.post("/predict")
def predict():
    """PLACEHOLDER — always returns the same fake result, regardless of
    input. Real implementation (Intern 3, SRS Day 6): accept a webcam
    frame, run MediaPipe hand-landmark detection + the trained classifier,
    and return the actual predicted sign and confidence."""
    return {
        "predicted_sign": "A",
        "confidence": 0.0,
        "note": "PLACEHOLDER RESPONSE — not a real prediction. Intern 3's real model replaces this.",
    }
