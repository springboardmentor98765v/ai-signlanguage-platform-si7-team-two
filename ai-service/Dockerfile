# ============================================================
# AI/CV service Dockerfile — PLACEHOLDER app (see ai-service/app/main.py).
#
# Unlike backend/, this placeholder doesn't need the db/ package (it has
# no database access), so build context can stay scoped to ai-service/.
# infra/docker-compose.yml still builds it with `context: ..` for
# consistency and so Intern 3 can freely import shared code later if
# needed without a compose file change.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY ai-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# NOTE: copying ai-service/'s CONTENTS into /app (not into /app/ai-service/)
# on purpose — "ai-service" has a hyphen, which is not a valid Python
# module name, so `uvicorn ai-service.app.main:app` would fail to import.
# This way the importable module is just `app.main:app`.
COPY ai-service/app/ ./app/

ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
