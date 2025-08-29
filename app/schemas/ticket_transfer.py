from pydantic import BaseModel
from app.models.ticket_transfer import TransferStatus
from datetime import datetime
from typing import Optional
#ticket transfer 
class TicketTransferRequest(BaseModel):
    ticket_id: int
    id: int
    from_agent_id: int
    to_agent_id: int
    request_reason: str
    status: TransferStatus
    resolved_by_admin_id: Optional[int] = None
    resolved_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class TicketTransferRequestUpdate(BaseModel):
    status: TransferStatus

    class Config:
        orm_mode = True
