# ============================================================
# Business Logic service Dockerfile
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY db/requirements.txt ./db-requirements.txt
COPY Bussiness_Logic/requirements.txt ./bl-requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt -r bl-requirements.txt

COPY db/ ./db/
COPY Bussiness_Logic/ ./Bussiness_Logic/

ENV PYTHONPATH=/app

EXPOSE 8002

CMD ["uvicorn", "Bussiness_Logic.main:app", "--host", "0.0.0.0", "--port", "8002"]
