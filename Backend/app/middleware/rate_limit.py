import time
from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT = 10
WINDOW = 60

requests = {}


async def rate_limit(request: Request, call_next):

    ip = request.client.host
    now = time.time()

    if ip not in requests:
        requests[ip] = []

    requests[ip] = [
        t for t in requests[ip]
        if now - t < WINDOW
    ]

    if len(requests[ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )

    requests[ip].append(now)

    return await call_next(request)