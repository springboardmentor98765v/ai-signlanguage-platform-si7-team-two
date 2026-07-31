# Robustness Testing Report

## Project

AI-Powered Sign Language Learning and Assessment Platform

---

# Objective

The objective of robustness testing is to evaluate the performance of the sign language recognition model under different real-world conditions. The tests assess how changes in lighting, background, camera position, distance, hand orientation, and users affect prediction accuracy.

---

# Model Information

- Model: XGBoost Classifier
- Input Features: 63 MediaPipe Hand Landmarks
- Number of Classes: 28
- Dataset Size: 2203 Samples
- Test Accuracy: 86.39%

---

# Test Environment

| Component | Details |
|-----------|---------|
| Operating System | Windows 11 |
| Webcam | Laptop Integrated Webcam |
| Framework | MediaPipe Hands |
| ML Library | XGBoost |
| Python Version | 3.11 |
| Camera Resolution | 640×480 |

---

# Test Scenarios

## RT-1 Normal Lighting

**Objective**

Evaluate prediction accuracy under normal indoor lighting.

**Procedure**

- Perform representative alphabet signs.
- Record predictions and confidence.

**Expected Result**

High prediction accuracy.

**Status**

PASS

---

## RT-2 Low Lighting

**Objective**

Evaluate model under dim lighting.

**Observation**

- Slight reduction in confidence.
- MediaPipe occasionally loses fingertip landmarks.

**Status**

PASS

---

## RT-3 Bright Lighting

**Objective**

Evaluate performance under bright lighting.

**Observation**

Prediction remained stable.

**Status**

PASS

---

## RT-4 Background Variation

**Objective**

Test different backgrounds.

Examples

- Plain wall
- Curtain
- Classroom
- Bookshelf

**Observation**

MediaPipe successfully isolated the hand in most cases.

**Status**

PASS

---

## RT-5 Camera Distance

Distances Tested

- 30 cm
- 50 cm
- 70 cm

**Observation**

- 50 cm produced the best accuracy.
- Very close distances caused landmark instability.
- Long distances reduced recognition confidence.

**Status**

PASS

---

## RT-6 Hand Rotation

Rotation Angles

- Slight
- Moderate

**Observation**

Misclassification increased for visually similar letters.

Examples

- M ↔ N
- U ↔ V
- R ↔ U

**Status**

PASS

---

## RT-7 Different User

Objective

Evaluate generalization on another user.

Observation

The model correctly recognized most alphabet signs with minor reductions in confidence.

Status

PASS

---

## RT-8 Camera Position

Positions Tested

- Eye Level
- Slightly Above
- Slightly Below

Observation

Recognition remained stable.

Status

PASS

---

## RT-9 Continuous Prediction

Objective

Run prediction continuously for approximately 15 minutes.

Observation

- No crashes
- Stable FPS
- No memory issues

Status

PASS

---

# Known Limitations

The model has difficulty distinguishing visually similar static signs.

Examples include:

- M and N
- U and V
- R and U
- E and S

Dynamic gestures such as Hello, Goodbye, and Thank You are outside the scope of the current static-image model.

---

# Conclusion

The AI model demonstrated stable performance across various environmental conditions including lighting, camera distance, backgrounds, and users. Minor performance degradation was observed under low lighting and rotated hand poses. Overall, the model satisfies the robustness requirements for Milestone 3.