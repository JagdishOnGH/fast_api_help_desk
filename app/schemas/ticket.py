
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .category import CategoryNameOnlyOut, SubcategoryNameOnlyOut, Category, Subcategory

from .user import UserOut # Assuming you have a UserOut schema in schemas/user.py
from app.models.ticket import TicketStatus, TicketPriority # Import enums from the model

class TicketBase(BaseModel):
    title: str
    initial_description: str

class TicketCreate(TicketBase):
    category_id: int
    subcategory_id: Optional[int] = None

class TicketUpdateStatus(BaseModel):
    status: TicketStatus

class TicketTransferRequestCreate(BaseModel):
    to_agent_id: int
    reason: Optional[str] = None

class Ticket(TicketBase):
    id: int
    ticket_uid: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime
    user: UserOut
    agent: Optional[UserOut] = None
    category: Category
    subcategory: Optional[Subcategory] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema for the Admin Dashboard
class DashboardStats(BaseModel):
    total_tickets: int
    resolved_tickets: int
    pending_tickets: int

#out

#messages

class TicketOut(TicketBase):
    id: int
    ticket_uid: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime
    user: UserOut
    agent: Optional[UserOut] = None
    category: CategoryNameOnlyOut
    subcategory: Optional[SubcategoryNameOnlyOut] = None
    
    class Config:
        from_attributes = True
