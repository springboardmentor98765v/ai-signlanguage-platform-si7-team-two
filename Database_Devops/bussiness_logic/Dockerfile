# ============================================================
# Business Logic service Dockerfile
# ============================================================

FROM python:3.11-slim

WORKDIR /app

# ------------------------------------------------------------
# Install database + business logic dependencies
# ------------------------------------------------------------

COPY Database_Devops/db/requirements.txt ./db-requirements.txt
COPY Bussiness_Logic/requirements.txt ./bl-requirements.txt

RUN pip install --no-cache-dir \
    -r db-requirements.txt \
    -r bl-requirements.txt

# ------------------------------------------------------------
# Copy database package
# ------------------------------------------------------------

COPY Database_Devops/db/ ./db/

# ------------------------------------------------------------
# Copy business logic application
# ------------------------------------------------------------

COPY Bussiness_Logic/ ./Bussiness_Logic/

# ------------------------------------------------------------
# Python configuration
# ------------------------------------------------------------

ENV PYTHONPATH=/app/Bussiness_Logic:/app

EXPOSE 8002

# ------------------------------------------------------------
# Start service
# ------------------------------------------------------------

CMD ["uvicorn", "Bussiness_Logic.main:app", "--host", "0.0.0.0", "--port", "8002"]