from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models.practice_model import PracticeSession
from schemas.practice_schema import (
    StartSessionRequest, StartSessionResponse,
    EndSessionRequest, EndSessionResponse
)

router = APIRouter(prefix="/practice", tags=["Practice Service"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start", response_model=StartSessionResponse)
def start_session(request: StartSessionRequest, db: Session = Depends(get_db)):
    new_session = PracticeSession(
        user_id=request.user_id,
        lesson_id=request.lesson_id,
        status="in_progress",
        attempt_count=0
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return StartSessionResponse(
        session_id=new_session.id,
        status=new_session.status,
        started_at=new_session.started_at
    )

@router.post("/attempt/{session_id}")
def log_attempt(session_id: str, db: Session = Depends(get_db)):
    session = db.query(PracticeSession).filter(PracticeSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.attempt_count += 1
    db.commit()
    db.refresh(session)

    return {"session_id": session.id, "attempt_count": session.attempt_count}

@router.post("/end", response_model=EndSessionResponse)
def end_session(request: EndSessionRequest, db: Session = Depends(get_db)):
    session = db.query(PracticeSession).filter(PracticeSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.ended_at = datetime.utcnow()
    session.status = "completed"
    db.commit()
    db.refresh(session)

    return EndSessionResponse(
        session_id=session.id,
        status=session.status,
        ended_at=session.ended_at,
        attempt_count=session.attempt_count
    )