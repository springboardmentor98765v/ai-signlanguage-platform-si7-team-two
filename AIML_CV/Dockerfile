# ============================================================
# AI/CV service Dockerfile — PLACEHOLDER app (see AIML_CV/app/main.py).
#
# Unlike Bussiness_Logic/, this placeholder doesn't need the Database_Devops/db/
# package (it has no database access), so build context can stay scoped to AIML_CV/.
# infra/docker-compose.yml still builds it with `context: ..` for
# consistency and so Intern 3 can freely import shared code later if
# needed without a compose file change.
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY AIML_CV/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# NOTE: copying AIML_CV/'s app/ CONTENTS into /app/ (not into /app/AIML_CV/)
# on purpose — keeping the importable module path simple as `app.main:app`.
COPY AIML_CV/app/ ./app/

ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
