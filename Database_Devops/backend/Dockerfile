# ============================================================
# Production Backend Dockerfile
# AI-Powered Sign Language Learning & Assessment Platform
#
# Build context:
#   Repository root
#
# This image packages:
#   - Backend/app -> /app/app
#   - Database_Devops/db -> /app/db
# ============================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install database and backend dependencies
COPY Database_Devops/db/requirements.txt ./db-requirements.txt
COPY Backend/requirements.txt ./backend-requirements.txt

RUN pip install --no-cache-dir \
    -r db-requirements.txt \
    -r backend-requirements.txt

# Copy shared database package
COPY Database_Devops/db/ ./db/

# Copy the current backend application
COPY Backend/app/ ./app/

# Backend API port
EXPOSE 8000

# Start the actual FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]