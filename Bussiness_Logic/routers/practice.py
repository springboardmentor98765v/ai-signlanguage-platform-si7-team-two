from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas.practice_schema import (
    StartSessionRequest, StartSessionResponse,
    EndSessionRequest, EndSessionResponse
)

router = APIRouter(prefix="/practice", tags=["Practice Service"])

sessions_db = {}
session_counter = 1

@router.post("/start", response_model=StartSessionResponse)
def start_session(request: StartSessionRequest):
    global session_counter
    session_id = session_counter
    session_counter += 1

    sessions_db[session_id] = {
        "user_id": request.user_id,
        "lesson_id": request.lesson_id,
        "expected_sign": request.expected_sign,
        "start_time": datetime.now(),
        "end_time": None,
        "status": "in_progress",
        "attempt_count": 0
    }

    return StartSessionResponse(
        session_id=session_id,
        status="in_progress",
        start_time=sessions_db[session_id]["start_time"]
    )

@router.post("/end", response_model=EndSessionResponse)
def end_session(request: EndSessionRequest):
    session = sessions_db.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["end_time"] = datetime.now()
    session["status"] = "completed"

    return EndSessionResponse(
        session_id=request.session_id,
        status="completed",
        end_time=session["end_time"],
        attempt_count=session["attempt_count"]
    )