#message base
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    ticket_id: int
    sender_id: int
    sender_name: str
    
    
    class Config:
        from_attributes = True

#message create

class MessageCreate(MessageBase):
    pass

#message out

class MessageOut(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

#Messages for ticket
#id, content, sender id, sender name,







