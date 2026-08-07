# Model Card

## Model Name

Sign Language Recognition Model (Milestone 3)

---

# Overview

This model is developed as part of the **AI-Powered Sign Language Learning and Assessment Platform**. It recognizes static American Sign Language (ASL) alphabet gestures using MediaPipe hand landmarks and an XGBoost classifier.

The model is designed to assist learners by providing real-time sign recognition, confidence scores, and automated assessment during practice sessions.

---

# Model Details

| Property | Value |
|----------|-------|
| Model Type | XGBoost Classifier |
| Framework | XGBoost |
| Computer Vision | MediaPipe Hands |
| Input | 21 Hand Landmarks (63 Features) |
| Output | Alphabet Prediction |
| Number of Classes | 28 |
| Language | American Sign Language (ASL) |
| Prediction Type | Multi-class Classification |

---

# Supported Classes

### Alphabet

```
A B C D E F G H I J
K L M N O P Q R S T
U V W X Y Z
```

### Additional Classes

```
DEL
SPACE
```

---

# Dataset

| Property | Value |
|----------|-------|
| Total Samples | 28203 |
| Features | 63 |
| Classes | 28 |
| Feature Type | MediaPipe Hand Landmarks |
| Preprocessing | Wrist-based Landmark Normalization |

Each sample contains:

```
x0,y0,z0,
x1,y1,z1,
...
x20,y20,z20
```

along with the corresponding class label.

---

# Feature Extraction

The model uses **MediaPipe Hands** to detect 21 hand landmarks from webcam images.

Each landmark contains:

- x coordinate
- y coordinate
- z coordinate

These values are flattened into a 63-dimensional feature vector and passed to the classifier.

---

# Training Pipeline

1. Collect dataset
2. Detect hand landmarks using MediaPipe
3. Extract landmark coordinates
4. Store features in CSV format
5. Encode labels using LabelEncoder
6. Split dataset into training and testing sets
7. Train XGBoost classifier
8. Save trained model
9. Evaluate model performance

---

# Hyperparameters

| Parameter | Value |
|-----------|------:|
| n_estimators | 300 |
| learning_rate | 0.05 |
| max_depth | 4 |
| subsample | 0.8 |
| colsample_bytree | 0.8 |

These values were obtained using RandomizedSearchCV hyperparameter tuning.

---

# Performance
Accuracy : 98.76%
Macro Precision : 98.46%
Macro Recall : 97.23%
Macro F1 Score : 97.76%
Weighted Precision : 98.9%
Weighted Recall : 98.8%
Weighted F1 Score : 98.8%

# Evaluation Artifacts

The following evaluation outputs are included in the project:

- Classification Report
- Confusion Matrix
- Confusion Matrix Heatmap
- Predictions CSV
- Weak Letters Report
- Metrics JSON

---

# Known Limitations

The model performs best on static alphabet signs.

Model Version

Version : 2.0

Dataset Size : 28,203

Training Time : 77.37 sec

Prediction Time : 0.3489 sec

Training Algorithm : XGBoost

Hyperparameter Tuning : RandomizedSearchCV

Feature Preprocessing : Wrist-based Landmark Normalization

# Intended Use

This model is intended for:

- Sign language learning
- Alphabet practice
- Educational assessment
- Student feedback

It is not intended for:

- Medical applications
- Emergency communication
- Official sign language interpretation
- Continuous sentence recognition

---

# Ethical Considerations

- The model is designed as an educational tool.
- Predictions may be incorrect under poor environmental conditions.
- Users should not rely on the model for critical communication.
- The dataset should contain diverse users to improve fairness and generalization.

---

# Future Improvements

Possible future enhancements include:

- Dynamic gesture recognition
- Word-level sign recognition
- Sentence recognition
- Two-hand sign detection
- Transformer/LSTM-based sequence models
- Larger and more diverse datasets
- Mobile device optimization

---

# Project Information

**Project:** AI-Powered Sign Language Learning and Assessment Platform

**Milestone:** Milestone 3

**AI Module:**

- MediaPipe Hand Landmark Detection
- Feature Extraction
- XGBoost Classification
- Real-Time Webcam Prediction
- Automated Assessment
- Confidence Score Generation