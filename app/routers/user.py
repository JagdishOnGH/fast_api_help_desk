from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.operations.user import get_user, get_users, create_user, update_user, delete_user
from app.dependencies import get_current_user
from app.models.user import UserRole
from app.operations.user import create_agent
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/add_user", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user


@router.post("/add_agent", response_model=UserOut)
def add_agent(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Role-based check
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add agents."
        )
    
    db_user = create_agent(db, user)
    return db_user





@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only the user themselves or admin can update
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user."
        )

    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only the user themselves or admin can delete
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
        )

    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
