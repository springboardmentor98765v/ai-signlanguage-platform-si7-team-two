# ============================================================
# AIML_CV service Dockerfile
#
# Build context must be the REPO ROOT so future imports from
# shared packages work without changing compose configuration.
# docker-compose.yml already sets `context: ..` for this service.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY AIML_CV/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY AIML_CV/ ./AIML_CV/

ENV PYTHONPATH=/app/AIML_CV:/app

EXPOSE 8001

CMD ["uvicorn", "AIML_CV.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
