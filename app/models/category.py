from sqlalchemy import Column, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete-orphan")

    # A category can have many agents assigned to it
    assigned_agents = relationship(
        "User",
        secondary="agent_category_assignments",
        back_populates="assigned_categories"
    )