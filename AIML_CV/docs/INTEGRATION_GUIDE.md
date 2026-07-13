# AI Service Integration Guide

# Overview

This document explains how the AI Prediction Service integrates with the Sign Language Learning and Assessment Platform.

The AI service is responsible for recognizing American Sign Language (ASL) hand gestures and returning the predicted sign with a confidence score.

---

# AI Service Responsibilities

The AI module performs the following tasks:

- Hand Detection
- Hand Landmark Extraction
- Feature Extraction
- Gesture Classification
- Confidence Estimation
- Prediction API

The AI service **does not** manage:

- User Authentication
- Database Operations
- Assessment Score Storage
- Course Management
- User Progress Tracking

These are handled by the Backend and Business Logic modules.

---

# Integration Architecture

```
Frontend (Intern 1)
        │
        ▼
Backend API (Intern 2)
        │
        ▼
Business Logic (Intern 4)
        │
        ▼
AI Prediction Service (Intern 3)
        │
        ▼
MediaPipe + XGBoost
```

---

# AI Prediction Endpoint

Base URL

```
http://127.0.0.1:8000
```

Endpoint

```
POST /predict
```

Content-Type

```
multipart/form-data
```

Parameter

| Name | Type |
|------|------|
| file | Image |

---

# Success Response

```json
{
    "prediction": "A",
    "confidence": 98.74
}
```

---

# Error Response

```json
{
    "success": false,
    "message": "No hand detected in the image."
}
```

---

# Integration Flow

1. User opens the Practice page.
2. Frontend accesses the user's webcam.
3. Frontend captures an image/frame.
4. Backend forwards the image to the AI Prediction Service.
5. AI service predicts the sign.
6. AI service returns prediction and confidence.
7. Backend processes the response.
8. Frontend displays the prediction.

---

# Frontend Responsibilities (Intern 1)

- Open webcam.
- Capture image/frame.
- Send image to Backend.
- Display prediction.
- Display confidence score.

---

# Backend Responsibilities (Intern 2)

- Receive image from Frontend.
- Forward request to AI service.
- Receive AI response.
- Return prediction to Frontend.

---

# Business Logic Responsibilities (Intern 4)

- Generate assessment questions.
- Compare prediction with expected sign.
- Calculate score.
- Store assessment results.
- Generate learner feedback.

---

# AI Responsibilities (Intern 3)

- Detect hand.
- Extract landmarks.
- Generate features.
- Predict sign.
- Return confidence score.
- Maintain AI prediction API.

---

# Notes

The AI service is independent of the frontend and backend implementation.

Any client capable of sending an image through HTTP can consume the prediction API.

Examples:

- React Application
- Android Application
- iOS Application
- Python Client
- Swagger UI

---

# Milestone 1 Integration Status

✔ AI Prediction API Completed

✔ FastAPI Integration Completed

✔ Swagger Testing Completed

✔ Backend Integration Ready

✔ Frontend Integration Ready

✔ Ready for End-to-End Testing