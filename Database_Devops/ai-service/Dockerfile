# Milestone 2, Day 9 — AI service Dockerfile, updated to package the
# trained model artifacts Intern 3 (Koushik) shared at the end of Day 9:
#   models/best_xgb_tuned.pkl
#   models/label_encoder.pkl
#
# Assumes Intern 3's existing FastAPI prediction app lives at app/main.py
# (built back in Milestone 1/2, Intern 3's track) — this file only adds the
# model artifacts and their dependencies for deployment. Adjust paths if
# the real repo's AI-service layout differs.

FROM python:3.11-slim

WORKDIR /app

# System deps commonly needed by opencv/mediapipe/xgboost wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (Intern 3's detection/prediction pipeline).
COPY app/ ./app/

# Trained model artifacts (Intern 3, shared end of Day 9).
# Drop the real files here before building:
#   ai-service/models/best_xgb_tuned.pkl
#   ai-service/models/label_encoder.pkl
COPY models/ ./models/

ENV MODEL_PATH=/app/models/best_xgb_tuned.pkl
ENV LABEL_ENCODER_PATH=/app/models/label_encoder.pkl

ENV PORT=8500
EXPOSE 8500

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
