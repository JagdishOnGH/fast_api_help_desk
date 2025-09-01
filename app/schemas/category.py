from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# ===================
# Subcategory Schemas
# ===================

class SubcategoryBase(BaseModel):
    """Base model with common attributes for a subcategory."""
    name: str
    description: Optional[str] = None

class SubcategoryCreate(SubcategoryBase):
    """Schema for creating a new subcategory (used in requests)."""
    pass

class Subcategory(SubcategoryBase):
    """Schema for reading a subcategory (used in responses)."""
    id: int
    
    # This enables Pydantic to read data from ORM models (SQLAlchemy objects)
    model_config = ConfigDict(from_attributes=True)

class SubcategoryOut(SubcategoryBase):
    """Schema for reading a subcategory (used in responses)."""
    id: int
    category_id: int
    name: str
    
    # This enables Pydantic to read data from ORM models (SQLAlchemy objects)
    model_config = ConfigDict(from_attributes=True)



# ===================
# Category Schemas
# ===================

class CategoryBase(BaseModel):
    """Base model with common attributes for a category."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""
    pass

class Category(CategoryBase):
    """
    Schema for reading a category.
    It includes a list of its associated subcategories for rich responses.
    """
    id: int
    subcategories: List[Subcategory] = []
    
    model_config = ConfigDict(from_attributes=True)


class CategoryOut(CategoryBase):
    """Schema for reading a category (used in responses)."""
    id: int
    subcategories: List[SubcategoryOut] = []
    
    model_config = ConfigDict(from_attributes=True)

#category nameonly out
class CategoryNameOnlyOut(BaseModel):
    """Schema for reading a category (used in responses)."""
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

#subcategories nameonly out
class SubcategoryNameOnlyOut(BaseModel):
    """Schema for reading a subcategory (used in responses)."""
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(CategoryBase):
    """Schema for updating a category."""
    pass

