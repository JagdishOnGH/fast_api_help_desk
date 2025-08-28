from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

class UserRole(PyEnum):
    user = "user"
    agent = "agent"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    profile_photo_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    created_tickets = relationship("Ticket", back_populates="user", foreign_keys="[Ticket.user_id]")
    
    # For an agent: tickets they are assigned to
    assigned_tickets = relationship("Ticket", back_populates="agent", foreign_keys="[Ticket.agent_id]")

    # For an agent: categories they are assigned to handle
    assigned_categories = relationship(
        "Category",
        secondary="agent_category_assignments",
        back_populates="assigned_agents"
    )
