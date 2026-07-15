# ============================================================
# Bussiness_Logic service Dockerfile
#
# IMPORTANT: build context must be the REPO ROOT, not Bussiness_Logic/,
# because this image needs the shared Database_Devops/db/ package
# (ORM models + engine) alongside the app code.
# docker-compose.yml already sets `context: ..` for this service.
# Don't docker build this directly from inside Bussiness_Logic/.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY Database_Devops/db/requirements.txt ./db-requirements.txt
COPY Bussiness_Logic/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt -r requirements.txt

COPY Database_Devops/db/ ./Database_Devops/db/
COPY Bussiness_Logic/ ./Bussiness_Logic/

ENV PYTHONPATH=/app/Bussiness_Logic:/app

EXPOSE 8000

CMD ["uvicorn", "Bussiness_Logic.main:app", "--host", "0.0.0.0", "--port", "8000"]
