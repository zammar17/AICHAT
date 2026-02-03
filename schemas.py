from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    user_input: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

class MessageRead(BaseModel):
    role: str
    content: str
    tokens: int
    cost: float

    class Config:
        from_attributes = True

class ChatSessionRead(BaseModel):
    id: str 
    created_at: datetime
    total_cost: float
    messages: List[MessageRead]

    class Config:
        from_attributes = True