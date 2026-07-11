# AI Prediction Service API Guide

## Overview

The AI Prediction Service is responsible for recognizing American Sign Language (ASL) hand gestures from an input image.

The service uses:

- MediaPipe Hands for hand landmark detection
- Feature Extraction (63 Features)
- XGBoost Classifier
- FastAPI REST API

---

## Base URL

```
http://127.0.0.1:8000
```

---

## Health Check

### Endpoint

```
GET /health
```

### Response

```json
{
    "status": "healthy"
}
```

---

## Predict Sign

### Endpoint

```
POST /predict
```

### Description

Accepts an image containing a hand gesture and predicts the corresponding ASL sign.

---

### Request

Content-Type

```
multipart/form-data
```

Parameter

| Name | Type | Required |
|------|------|----------|
| file | Image | Yes |

Supported formats

- JPG
- JPEG
- PNG

---

### Success Response

Status Code

```
200 OK
```

Example

```json
{
    "prediction": "A",
    "confidence": 98.74
}
```

---

### Error Responses

#### Invalid Image

```json
{
    "success": false,
    "message": "Invalid image uploaded."
}
```

---

#### No Hand Detected

```json
{
    "success": false,
    "message": "No hand detected in the image."
}
```

---

## Processing Pipeline

Input Image

↓

MediaPipe Hand Detection

↓

21 Hand Landmarks

↓

63 Landmark Features

↓

XGBoost Model

↓

Prediction

↓

JSON Response

---

## Notes

- Only one hand is supported.
- Images should contain a clearly visible hand.
- Confidence is returned as a percentage.
- Images are processed in RGB format internally.

---

## Example cURL Request

```bash
curl -X POST \
"http://127.0.0.1:8000/predict" \
-F "file=@A.jpg"
```

---

## Example Response

```json
{
    "prediction": "A",
    "confidence": 98.74
}
```