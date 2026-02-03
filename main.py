from math import cos
from fastapi import FastAPI, Depends, HTTPException
from openai.types.beta import assistant
from sqlalchemy.orm import Session
import uuid

from sqlalchemy.sql.functions import user

import models
import schemas
import service
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chat API",
    description="A simple API for AI chat sessions and calculating costs based on token usage.",
    version="1.0.0"
)

@app.post("/sessions/", response_model=schemas.ChatSessionRead, tags=["Sessions"])
def create_session(db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    db_session = models.ChatSession(id=session_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.post("/sessions/{session_id}/message/", tags=["Messages"])
def send_message(session_id: str, payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found :(")
    
    history = [{"role": m.role, "content": m.content} for m in session.messages]
    history.append({"role": "user", "content": payload.user_input})

    ai_data = service.get_openai_response(history)

    user_msg = models.Message(
        session_id=session_id,
        role="user",
        content=payload.user_input,
        tokens=0,
        cost=0.0
    )

    assistant_msg = models.Message(
        session_id=session_id,
        role="assistant",
        content=ai_data["content"],
        tokens=ai_data["tokens"],
        cost=ai_data["cost"]
    )

    session.total_cost += ai_data["cost"]

    db.add_all([user_msg, assistant_msg])
    db.commit()

    return {
        "reply": ai_data["content"],
        "session_cost": session.total_cost,
        "tokens_used": ai_data["tokens"],
    }

@app.get("/sessions/{session_id}/", response_model=schemas.ChatSessionRead, tags=["Sessions"])
def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found :(")
    return session

@app.delete("/sessions/{session_id}/", tags=["Sessions"])
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found :(")
    
    db.delete(session)
    db.commit()
    return {"status": "Success", "message": f"Session {session_id} deleted."}    