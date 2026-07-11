# AI Processing Pipeline

# Sign Language Recognition Pipeline

## Overview

The Sign Language Recognition pipeline converts an input image into a predicted American Sign Language (ASL) alphabet using Computer Vision and Machine Learning.

The pipeline consists of multiple stages, from image acquisition to prediction generation.

---

# Complete Pipeline

```
Input Image
     │
     ▼
Image Preprocessing
(OpenCV)
     │
     ▼
MediaPipe Hand Detection
     │
     ▼
21 Hand Landmarks
     │
     ▼
Feature Extraction
(63 Features)
     │
     ▼
XGBoost Classifier
     │
     ▼
Prediction
     │
     ▼
Confidence Score
     │
     ▼
JSON Response
```

---

# Stage 1 - Image Acquisition

Source

- Webcam
- Uploaded Image
- Frontend Camera Frame

Accepted Formats

- JPG
- JPEG
- PNG

The input image is received by the FastAPI service.

---

# Stage 2 - Image Preprocessing

Library

OpenCV

Operations Performed

- Read Image
- Decode Image
- Convert BGR to RGB

Reason

MediaPipe expects RGB images.

---

# Stage 3 - Hand Detection

Library

MediaPipe Hands

Configuration

Maximum Hands

1

Detection Confidence

0.5

Tracking Confidence

0.5

Output

21 Hand Landmarks

If no hand is detected, the API returns:

```json
{
    "success": false,
    "message": "No hand detected in the image."
}
```

---

# Stage 4 - Feature Extraction

Each landmark contains

- X Coordinate
- Y Coordinate
- Z Coordinate

Total Features

21 × 3

=

63 Features

Example

```
x0 y0 z0

x1 y1 z1

...

x20 y20 z20
```

The extracted features form the input vector for the Machine Learning model.

---

# Stage 5 - Machine Learning Prediction

Algorithm

XGBoost Classifier

Input

63 Landmark Features

Output

Predicted Sign

Confidence Score

Example

Prediction

A

Confidence

98.74%

---

# Stage 6 - Response Generation

The FastAPI service converts the prediction into a JSON response.

Example

```json
{
    "prediction": "A",
    "confidence": 98.74
}
```

---

# Complete Request Flow

```
Frontend

        │

        ▼

POST /predict

        │

        ▼

FastAPI Router

        │

        ▼

Recognizer Service

        │

        ▼

MediaPipe

        │

        ▼

Feature Extractor

        │

        ▼

Predictor

        │

        ▼

XGBoost Model

        │

        ▼

Prediction

        │

        ▼

JSON Response
```

---

# Project Architecture

```
Client
│
├── React Frontend
│
└── Swagger UI
        │
        ▼
FastAPI
│
├── Routes
│
├── Schemas
│
├── Exception Handler
│
└── Logger
        │
        ▼
Recognizer Service
        │
        ▼
Feature Extraction
        │
        ▼
Inference
        │
        ▼
XGBoost Model
```

---

# Performance

Average Pipeline

Image

↓

MediaPipe Detection

↓

Feature Extraction

↓

Prediction

↓

Response

Processing Time

Typically less than one second on a standard laptop.

---

# Advantages

- Modular Architecture
- Fast Inference
- Lightweight
- Easy Backend Integration
- REST API Based
- Frontend Independent
- Scalable

---

# Future Pipeline

```
Live Webcam

↓

Frame Stream

↓

MediaPipe

↓

Gesture Tracking

↓

Temporal Model

↓

Sentence Formation

↓

Text Generation

↓

Speech Synthesis
```

This represents the future roadmap of the Sign Language Learning and Assessment Platform.
                User
                  │
                  ▼
          React Frontend
                  │
                  ▼
        FastAPI Prediction API
                  │
                  ▼
      SignLanguageRecognizer
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
MediaPipe Hands         XGBoost Model
      │
      ▼
Feature Extraction (63 Features)
                  │
                  ▼
         Prediction + Confidence
                  │
                  ▼
              JSON Response