from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import datetime

class ChatSession(Base):
    __tablename__ = 'sessions'

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    total_cost = Column(Float, default=0.0)

    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey('sessions.id'))
    role = Column(String)
    content = Column(String)
    tokens = Column(Integer)
    cost = Column(Float)

    session = relationship("ChatSession", back_populates="messages")