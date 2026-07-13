# ============================================================
# Backend service Dockerfile — PLACEHOLDER app (see Bussiness_Logic/app/main.py).
#
# IMPORTANT: build context must be the REPO ROOT, not Bussiness_Logic/, because
# this image needs the shared Database_Devops/db/ package (ORM models + engine)
# alongside the backend app code. infra/docker-compose.yml is already set up with
# `context: ..` for this service — don't `docker build` this file directly
# from inside Bussiness_Logic/, it will fail to find Database_Devops/db/.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY Database_Devops/db/requirements.txt ./db-requirements.txt
COPY Bussiness_Logic/requirements.txt ./backend-requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt -r backend-requirements.txt

COPY Database_Devops/db/ ./Database_Devops/db/
COPY Bussiness_Logic/ ./Bussiness_Logic/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "Bussiness_Logic.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
