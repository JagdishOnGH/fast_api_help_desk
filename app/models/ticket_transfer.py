from sqlalchemy import Column, Integer, Text, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum

class TransferStatus(PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class TicketTransfer(Base):
    __tablename__ = "ticket_transfers"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    from_agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_reason = Column(Text)
    status = Column(Enum(TransferStatus), default=TransferStatus.pending, nullable=False)
    requested_at = Column(TIMESTAMP, server_default=func.now())
    resolved_by_admin_id = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(TIMESTAMP)

    ticket = relationship("Ticket")
    from_agent = relationship("User", foreign_keys=[from_agent_id])
    to_agent = relationship("User", foreign_keys=[to_agent_id])
    resolved_by_admin = relationship("User", foreign_keys=[resolved_by_admin_id])

