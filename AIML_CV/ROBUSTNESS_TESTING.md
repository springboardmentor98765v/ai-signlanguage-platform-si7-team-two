# Robustness Testing — Sign Language Recognition Model

**Owner:** Intern 3 (AI/ML & CV)
**Milestone:** 1
**Last Updated:** July 2026

---

## Overview

This document describes the robustness testing approach for the XGBoost + MediaPipe sign language recognition model. Tests cover classification accuracy, confidence threshold behaviour, edge cases, and REST API error handling.

---

## Test Coverage

### 1. Unit Tests — `tests/`

Located in `tests/` directory. Run from repo root:

```bash
cd AIML_CV
pytest tests/ -v
```

Key test scenarios:

| Test | Description |
|---|---|
| `test_predictor.py` | `predict_sign()` with valid 63-feature input → returns `(str, float)` |
| `test_recognizer.py` | `SignLanguageRecognizer.predict()` with no-hand frame → `prediction == "No Hand"` |
| Confidence threshold | Features producing confidence < 0.80 → label is `"Unknown"` |

### 2. Integration / API Tests — `test_recognizer.py` (root)

```bash
python test_recognizer.py
```

Tests the full pipeline against images in `test_images/` (if populated).

---

## Edge Case Handling

| Scenario | Expected Behaviour |
|---|---|
| No hand detected in frame | Returns `{"prediction": "No Hand", "confidence": 0.0}` |
| Low confidence (< 0.80) | Returns `{"prediction": "Unknown", "confidence": <raw_value>}` |
| Invalid/corrupt image upload | API raises HTTP 400 with `"Invalid image uploaded."` |
| Multiple hands in frame | Only the **first** detected hand is used (`multi_hand_landmarks[0]`) |
| Empty image (all zeros) | MediaPipe returns no landmarks → `"No Hand"` |

---

## Confidence Threshold Rationale

The 0.80 threshold (`THRESHOLD = 0.80` in `inference/predictor.py`) was chosen to minimize false-positive sign classifications. Signs with visually similar hand shapes (e.g., A/S/E, M/N) tend to score < 0.80 on ambiguous frames, making `"Unknown"` the safer response than a wrong label.

The `/predict` API additionally raises HTTP 400 on `"No Hand"` — the assessment engine should not attempt to score an attempt where no hand was detected.

---

## Known Limitations & Failure Modes

| Limitation | Impact | Mitigation |
|---|---|---|
| Training data distribution unknown | May underperform on certain skin tones / lighting conditions | Collect diverse test images; augment training set |
| Static-image model | Reduced accuracy on fast-moving hands | Use prediction smoothing (`deque(maxlen=5)` in `assessment_app.py`) |
| Single-hand only | Multi-hand signs not supported in this version | Documented limitation for Milestone 1 |
| MediaPipe version sensitivity | `mediapipe==0.10.14` required; earlier versions have different landmark indices | Pinned in `requirements.txt` |

---

## Test Images

Place test images in `test_images/` directory for manual validation. Not committed to Git (add to `.gitignore` if containing sensitive frames).

---

## Future Testing (Milestone 2+)

- [ ] Cross-lighting condition tests (bright/dark/backlit)
- [ ] Cross-skin-tone evaluation
- [ ] Benchmark against held-out test split (accuracy, F1 per class)
- [ ] Load test `/predict` endpoint under concurrent requests
