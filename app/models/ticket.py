from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum

class TicketStatus(PyEnum):
    open = "open"
    assigned = "assigned"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"
    reopened = "reopened"
    requested_reopen = "requested_reopen"
    

class TicketPriority(PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_uid = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id",  ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    initial_description = Column(Text, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.open, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.medium, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    closed_at = Column(TIMESTAMP, nullable=True)
    

   
    messages = relationship("Message", back_populates="ticket")

    notes = relationship("TicketNote", back_populates="ticket")
    
    user = relationship("User", back_populates="created_tickets", foreign_keys=[user_id])
    
    # Link to the agent assigned to the ticket
    agent = relationship("User", back_populates="assigned_tickets", foreign_keys=[agent_id])

    # Link to the ticket's category
    category = relationship("Category")
    
    # Link to the ticket's subcategory
    subcategory = relationship("Subcategory")

