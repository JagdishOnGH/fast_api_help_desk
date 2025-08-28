from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TicketNote(Base):
    __tablename__ = "ticket_notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    ticket = relationship("Ticket", back_populates="notes")
    agent = relationship("User")
