# Model Documentation

# Sign Language Recognition AI Model

## 1. Overview

The Sign Language Recognition AI model is designed to recognize American Sign Language (ASL) hand gestures from static images.

The system uses Computer Vision and Machine Learning to identify hand signs and return the predicted alphabet along with the confidence score.

---

# 2. Objective

The objective of this model is to:

- Detect a hand from an input image.
- Extract meaningful hand landmark features.
- Classify the hand gesture into an ASL sign.
- Return the predicted sign and confidence score.

---

# 3. Dataset

Dataset Name

ASL Hand Landmark Dataset

Source

Kaggle

Number of Classes

28

Classes

- A-Z (26 Alphabets)
- del
- space

Total Samples

2203

---

# 4. Feature Extraction

The system uses Google's MediaPipe Hands solution.

MediaPipe detects:

- 21 Hand Landmarks

Each landmark contains:

- X Coordinate
- Y Coordinate
- Z Coordinate

Therefore,

21 × 3 = 63 Features

Example

x0 y0 z0

x1 y1 z1

...

x20 y20 z20

These 63 features are used as the input to the Machine Learning model.

---

# 5. Data Preprocessing

The dataset is divided into:

Training Set

80%

Testing Set

20%

Train-Test Split

Random State = 42

The label column is encoded using LabelEncoder.

---

# 6. Machine Learning Models Evaluated

The following models were trained and compared.

| Model | Accuracy |
|--------|-----------|
| K-Nearest Neighbors | 70.98% |
| Random Forest | 80.95% |
| Support Vector Machine | 80.73% |
| XGBoost | **85.71%** |

XGBoost achieved the highest accuracy and was selected as the final model.

---

# 7. Final Model

Algorithm

XGBoost Classifier

Advantages

- High prediction accuracy
- Fast inference
- Robust to noisy data
- Handles multiclass classification efficiently

Saved Model

models/best_xgb_tuned.pkl

---

# 8. Model Performance

Accuracy

85.71%

Prediction Output

- Predicted Sign
- Confidence Score

Example

Prediction

A

Confidence

98.74%

---

# 9. Prediction Pipeline

Input Image

↓

MediaPipe Hand Detection

↓

21 Hand Landmarks

↓

63 Landmark Features

↓

XGBoost Classifier

↓

Predicted Sign

↓

Confidence Score

↓

JSON Response

---

# 10. API Integration

The trained model is exposed through a FastAPI REST API.

Endpoint

POST /predict

Input

Image File

Output

```json
{
    "prediction": "A",
    "confidence": 98.74
}
```

---

# 11. Configuration

Maximum Hands

1

Minimum Detection Confidence

0.5

Minimum Tracking Confidence

0.5

Prediction Confidence Threshold

80%

Temporal Smoothing Window

5 Frames

---

# 12. Project Structure

models/

- best_xgb_tuned.pkl
- label_encoder.pkl

services/

- recognizer.py

inference/

- predictor.py

src/

- feature_extractor.py

api/

- prediction.py

---

# 13. Limitations

Current limitations include:

- Supports only one hand.
- Static ASL alphabet recognition.
- Requires adequate lighting.
- Performance decreases with severe hand occlusion.
- Background clutter may reduce detection accuracy.

---

# 14. Future Improvements

Possible future enhancements include:

- Dynamic sign recognition.
- Sentence formation.
- Continuous sign language recognition.
- Transformer-based gesture recognition.
- Deep Learning (CNN + LSTM).
- Multi-hand recognition.
- Real-time sentence generation.

---

# 15. Technologies Used

Programming Language

- Python

Computer Vision

- OpenCV
- MediaPipe

Machine Learning

- XGBoost
- Scikit-learn

Backend

- FastAPI

API Testing

- Swagger UI

---

# 16. Conclusion

The Sign Language Recognition AI model successfully recognizes ASL hand gestures using MediaPipe hand landmarks and an XGBoost classifier.

The model achieved an accuracy of 85.71% and is deployed as a FastAPI microservice, making it ready for integration with the frontend and backend components of the Sign Language Learning and Assessment Platform.