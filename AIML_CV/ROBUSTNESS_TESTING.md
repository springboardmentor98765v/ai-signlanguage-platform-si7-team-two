# Robustness Testing Report

## Project

**Sign Language Learning and Assessment Platform**

AI/ML & Computer Vision Module

---

# Objective

The objective of robustness testing is to evaluate how well the sign language recognition model performs under different real-world conditions.

The tests focus on:

- Lighting
- Camera distance
- Hand orientation
- Background complexity
- Different users
- Partial occlusion

---

# Test Environment

Operating System:

Windows 11

Camera:

Laptop Webcam

Frameworks:

- MediaPipe
- OpenCV
- FastAPI
- XGBoost

---

# Test Cases

## 1. Normal Lighting

Condition:

Indoor room lighting.

Expected:

Correct sign recognition.

Result:

✅ Passed

Observation:

Prediction confidence remained consistently high (>95%).

---

## 2. Low Lighting

Condition:

Dim room.

Expected:

Recognition accuracy may decrease.

Result:

⚠ Partial Pass

Observation:

MediaPipe occasionally failed to detect hand landmarks.

---

## 3. Bright Lighting

Condition:

Bright LED lighting.

Expected:

Stable predictions.

Result:

✅ Passed

Observation:

No significant degradation observed.

---

## 4. Camera Distance

### Close Distance

Result:

✅ Passed

Average confidence remained above 95%.

---

### Medium Distance

Result:

✅ Passed

Stable predictions.

---

### Long Distance

Result:

⚠ Partial Pass

Hand landmarks became less accurate due to reduced hand size.

---

## 5. Background Complexity

### Plain Background

Result:

✅ Passed

Recognition remained stable.

---

### Busy Background

Result:

⚠ Partial Pass

Occasional landmark instability.

---

## 6. Hand Rotation

Condition:

Different hand orientations.

Result:

⚠ Partial Pass

Extreme rotations reduced prediction confidence.

---

## 7. Partial Occlusion

Condition:

Some fingers hidden.

Result:

❌ Failed

Prediction accuracy decreased significantly.

Reason:

MediaPipe could not estimate hidden landmarks reliably.

---

## 8. Different Users

Condition:

Different hand sizes and skin tones.

Result:

✅ Passed

Normalization using MediaPipe landmarks enabled consistent predictions.

---

# Failure Cases

Observed failure scenarios:

- Hand outside camera frame
- Heavy finger occlusion
- Very low lighting
- Motion blur
- Incorrect hand orientation

The system correctly returns:

```json
{
    "prediction": "No Hand",
    "confidence": 0.0
}
```

when no hand is detected.

---

# Model Limitations

Current model supports:

- Single hand
- Static signs

Current model does not support:

- Dynamic gestures
- Continuous sentence recognition
- Two-hand signs
- Severe occlusion

---

# Future Improvements

Potential enhancements:

- Temporal models (LSTM/Transformer)
- Multi-hand detection
- Larger datasets
- Data augmentation
- Automatic feedback using landmark analysis
- Personalized learning analytics

---

# Overall Assessment

The model performs reliably under standard operating conditions.

Best performance is achieved with:

- Good lighting
- Plain background
- Single visible hand
- Front-facing camera

Overall robustness is suitable for educational sign language learning and assessment.