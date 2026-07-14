1. Start server

uvicorn app.main:app --reload

2. Open Swagger

http://127.0.0.1:8000/docs

3. Test

GET /

GET /health

POST /auth/register

POST /auth/login

Expected responses...