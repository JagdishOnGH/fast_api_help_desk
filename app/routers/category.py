"""
1 protected routes, Create, Update, Delete, can be done by user with roles admin and agent
2 List and List by id are open to all
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.dependencies import get_current_user # Assuming you have a general get_current_user
from app.operations import category as category_ops
from app.schemas import category as category_schema
from app.models.user import UserRole
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models import User 

router = APIRouter(prefix="/categories", tags=["Categories"])

# Dependency

@router.get("/", response_model=List[category_schema.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    
):
    """
   every user can see all categories and subcategories count
    """
    return category_ops.all_categories(db)

#everybody can see category by id, having subcategories(Id, Name)
@router.get("/{category_id}", response_model=category_schema.Category)
def read_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    
):
    """
    Retrieves a category by ID, including its subcategories.
    """
    return category_ops.category_by_id(db, category_id)

#only admin and agent can create, update, delete category
@router.post("/", response_model=category_schema.Category)
def create_category(
    category_data: category_schema.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    """
    Creates a new category.
    """
    if(current_user.role != UserRole.admin and current_user.role != UserRole.agent):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create a category.")
    return category_ops.create_category(db, category_data)

@router.put("/{category_id}", response_model=category_schema.Category)
def update_category(
    category_id: int,
    category_data: category_schema.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates an existing category.
    """
    if(current_user.role != UserRole.admin and current_user.role != UserRole.agent):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update a category.")
    return category_ops.update_category(db, category_id, category_data)

@router.delete("/{category_id}", response_model=category_schema.Category)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes a category.
    """
    if(current_user.role != UserRole.admin and current_user.role != UserRole.agent):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete a category.")
    return category_ops.delete_category(db, category_id)

