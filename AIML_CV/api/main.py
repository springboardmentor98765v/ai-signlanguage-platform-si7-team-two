from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

import cv2
import numpy as np

from services.recognizer import SignLanguageRecognizer

app = FastAPI(
    title="Sign Language Assessment API"
)

recognizer = SignLanguageRecognizer()


@app.get("/")
def home():

    return {
        "message": "Sign Language Assessment API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()

    np_image = np.frombuffer(image_bytes, np.uint8)

    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = recognizer.predict(rgb)

    response = {
        "prediction": result["prediction"],
        "confidence": round(float(result["confidence"]) * 100, 2)
    }

    return JSONResponse(content=response)