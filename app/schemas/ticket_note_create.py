from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketNoteCreate(BaseModel):
    note: str
    
    
class TicketNoteUpdate(BaseModel):
    note: Optional[str] = None


#out

class TicketNoteOut(BaseModel):
    id: int
    note: str
    ticket_id: int
    agent_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
