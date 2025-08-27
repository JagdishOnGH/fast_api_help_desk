from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class AgentCategoryAssignment(Base):
    __tablename__ = "agent_category_assignments"

    agent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
