from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role=UserRole.user,
        profile_photo_url=user.profile_photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def create_agent(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role=UserRole.agent,
        profile_photo_url=user.profile_photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# def create_admin(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role=UserRole.admin,
        profile_photo_url=user.profile_photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    if user.name:
        db_user.name = user.name
    if user.password:
        from app.core.security import get_password_hash
        db_user.password_hash = get_password_hash(user.password)
    if user.profile_photo_url:
        db_user.profile_photo_url = user.profile_photo_url
    db.commit()
    db.refresh(db_user)
    return db_user

 

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
