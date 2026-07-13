# ============================================================
# Backend service Dockerfile — PLACEHOLDER app (see backend/app/main.py).
#
# IMPORTANT: build context must be the REPO ROOT, not backend/, because
# this image needs the shared db/ package (ORM models + engine) alongside
# the backend app code. infra/docker-compose.yml is already set up with
# `context: ..` for this service — don't `docker build` this file directly
# from inside backend/, it will fail to find db/.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY db/requirements.txt ./db-requirements.txt
COPY backend/requirements.txt ./backend-requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt -r backend-requirements.txt

COPY db/ ./db/
COPY backend/ ./backend/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
