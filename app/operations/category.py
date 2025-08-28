# Category Operations and Subcategory Operations

"""
1 Create Category
2 Create Subcategory
3 Update Category
4 Update Subcategory
5 Delete Category
6 Delete Subcategory
7 All categories and count of subcategories
8 Category id provided to see list of name of cat and subcategories[ {id, name} ]
"""

from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.schemas.category import Category as category_schema
from app.schemas.category import Subcategory as subcategory_schema
from app.schemas.category import CategoryOut as category_out_schema
from app.schemas.category import SubcategoryOut as subcategory_out_schema

def create_category(db: Session, category_data: category_schema):
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
    
def create_subcategory(db: Session, subcategory_data: subcategory_schema):
    db_subcategory = Subcategory(**subcategory_data.model_dump())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

def update_category(db: Session, category_data: category_schema):
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_subcategory(db: Session, subcategory_data: subcategory_schema):
    db_subcategory = Subcategory(**subcategory_data.model_dump())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

def delete_category(db: Session, category_id: int):
    db_category = Category(**category_data.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_subcategory(db: Session, subcategory_id: int):
    db_subcategory = Subcategory(**subcategory_data.model_dump())
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory

def all_categories(db: Session):
    return db.query(Category).all()

def category_by_id(db: Session, category_id: int):
   #id,name and subcategories(name, id)
   return db.query(Category).filter(Category.id == category_id).first()
