# 🤟 AI-Powered Sign Language Learning and Assessment Platform

An AI-powered educational platform that helps users learn and practice **American Sign Language (ASL)** alphabets through real-time hand gesture recognition and automated assessment.

This project was developed as part of **Milestone 3** and uses **Computer Vision**, **MediaPipe**, and **Machine Learning** to recognize static ASL alphabet signs from webcam input.

---

## 📌 Features

- ✨ Real-time ASL alphabet recognition
- 🖐️ MediaPipe Hand Landmark Detection
- 🤖 XGBoost-based gesture classification
- 📊 Confidence score generation
- 📝 Interactive assessment mode
- 🎯 Automatic scoring and feedback
- ⚡ Fast real-time prediction
- 🌐 REST API for backend integration

---

## 🏗️ Project Architecture

```
Webcam
   │
   ▼
MediaPipe Hands
   │
21 Hand Landmarks
   │
Feature Extraction (63 Features)
   │
XGBoost Classifier
   │
Prediction + Confidence
   │
Assessment Engine / API
```

---

## 📂 Project Structure

```
AIML_CV/
│
├── api/                     # FastAPI backend
├── assessment/              # Assessment engine
├── config/                  # Configuration
├── dataset/                 # Training dataset
├── docs/                    # Documentation
├── evaluation/              # Model evaluation
├── experiments/             # Training & tuning scripts
├── inference/               # Prediction pipeline
├── models/                  # Trained models
├── services/                # Prediction services
├── src/                     # Feature extraction modules
├── tests/                   # Test cases
├── test_images/             # Sample images
│
├── assessment_app.py
├── MODEL_CARD.md
├── ROBUSTNESS_TESTING.md
├── requirements.txt
└── README.md
```

---

# 🧠 AI Model

| Property   | Value                      |
| ---------- | -------------------------- |
| Model      | XGBoost Classifier         |
| Input      | 21 Hand Landmarks          |
| Features   | 63                         |
| Classes    | 28                         |
| Prediction | Multi-class Classification |

---

## 📊 Dataset

| Property | Value |
| -------- | ----- |
| Samples  | 2203  |
| Classes  | 28    |
| Features | 63    |

Supported Classes

```
A-Z
DEL
SPACE
```

---

# ⚙️ Hyperparameters

The final model was obtained after hyperparameter tuning using **RandomizedSearchCV**.

| Parameter        | Value |
| ---------------- | ----: |
| n_estimators     |   300 |
| learning_rate    |  0.05 |
| max_depth        |     4 |
| subsample        |   0.8 |
| colsample_bytree |   0.8 |

Final trained model:

```
models/best_xgb_tuned.pkl
```

---

# 📈 Performance

| Metric            |  Score |
| ----------------- | -----: |
| Accuracy          | 86.39% |
| Macro F1 Score    | 86.67% |
| Weighted F1 Score | 86.52% |

Evaluation artifacts include:

- Classification Report
- Confusion Matrix
- Confusion Matrix Heatmap
- Metrics JSON
- Prediction Report
- Weak Letter Analysis

---

# 🧪 Robustness Testing

The model was evaluated under multiple real-world conditions.

Tests performed:

- ✅ Normal lighting
- ✅ Low lighting
- ✅ Bright lighting
- ✅ Different backgrounds
- ✅ Camera distance variations
- ✅ Hand rotation
- ✅ Different users
- ✅ Continuous prediction

The model demonstrated stable performance across varying environmental conditions while maintaining reliable real-time inference.

Detailed report:

```
ROBUSTNESS_TESTING.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
cd AIML_CV
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

### Assessment Application

```bash
python assessment_app.py
```

### API

```bash
uvicorn api.main:app --reload
```

---

# 📡 API Endpoints

| Method | Endpoint   | Description  |
| ------ | ---------- | ------------ |
| GET    | `/health`  | Health check |
| POST   | `/predict` | Predict sign |

---

# 📚 Documentation

Additional documentation is available in:

- MODEL_CARD.md
- ROBUSTNESS_TESTING.md
- docs/PIPELINE.md
- docs/MODEL_DOCUMENTATION.md
- docs/AI_API_GUIDE.md
- docs/INTEGRATION_GUIDE.md

---

# 🔮 Future Improvements

- Dynamic gesture recognition
- Word-level recognition
- Sentence recognition
- Two-hand gesture support
- Mobile application deployment
- Deep Learning sequence models (LSTM/Transformer)

---

# 👥 Team

**Project:** AI-Powered Sign Language Learning and Assessment Platform

**Milestone:** Milestone 3

**Module:** AI/ML & Computer Vision

---

# 📄 License

This project was developed for educational purposes as part of an academic internship project.
