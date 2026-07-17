# Model Card – Sign Language Recognition Model

## Model Overview

**Model Name:** Sign Language Recognition using XGBoost

**Version:** 1.0

**Author:** Koushik Goud E

**Project:** Sign Language Learning and Assessment Platform

**Internship:** Infosys Springboard Virtual Internship 7.0

**Role:** AI/ML & Computer Vision Engineer

---

# Purpose

This model recognizes American Sign Language (ASL) hand signs from images using MediaPipe hand landmarks and an XGBoost classifier.

The model is integrated into a Sign Language Learning and Assessment Platform to:

- Recognize hand signs
- Provide confidence scores
- Give learner-friendly feedback
- Assist in sign language practice and assessment

---

# Supported Classes

The model recognizes **28 classes**:

- A
- B
- C
- D
- E
- F
- G
- H
- I
- J
- K
- L
- M
- N
- O
- P
- Q
- R
- S
- T
- U
- V
- W
- X
- Y
- Z
- del
- space

---

# Input

RGB image containing a single hand.

MediaPipe extracts:

- 21 hand landmarks

Each landmark contains:

- x
- y
- z

Total features:

63

---

# Feature Extraction

Feature extraction uses MediaPipe Hands.

Each sample contains:

```
x0,y0,z0
...
x20,y20,z20
```

Total:

63 numerical features.

---

# Machine Learning Model

Algorithm:

- XGBoost Classifier

Reason for selection:

- High accuracy
- Fast inference
- Handles tabular landmark features efficiently
- Robust compared to KNN, Random Forest, and SVM

---

# Dataset

Dataset:

```
asl_landmarks_final.csv
```

Contains:

- MediaPipe hand landmarks
- 28 sign classes

Training/Test split:

80% Training

20% Testing

---

# Performance

Model Accuracy:

**85.71%**

Evaluation metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix
- Classification Report

---

# API Output

The prediction API returns:

```json
{
  "prediction": "B",
  "confidence": 97.30,
  "possible_issue": "Excellent! Your sign looks correct."
}
```

---

# Feedback System

The application provides confidence-based feedback.

Confidence ≥ 95%

- Excellent! Your sign looks correct.

Confidence 85–95%

- Good attempt with sign-specific guidance.

Confidence < 85%

- Try again with sign-specific guidance.

---

# Technologies Used

- Python
- FastAPI
- OpenCV
- MediaPipe
- NumPy
- Scikit-learn
- XGBoost

---

# Known Limitations

Current model assumes:

- Single hand only
- Good lighting conditions
- Hand fully visible
- Front-facing camera
- Static sign recognition

Dynamic gestures such as motion-based signs are not fully evaluated.

---

# Ethical Considerations

This model is intended for educational purposes.

It should not be used as a medical, legal, or accessibility certification tool.

Predictions should be considered assistive rather than authoritative.

---

# Future Improvements

Potential enhancements include:

- Dynamic gesture recognition
- Two-hand sign support
- Larger and more diverse datasets
- Personalized learner feedback
- Real-time sentence recognition
- Transformer or deep learning based models

---

# Model Version

Version: 1.0

Last Updated:

July 2026