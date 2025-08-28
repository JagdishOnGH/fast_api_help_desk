from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    agent = "agent"
    admin = "admin"

# Schema for reading user data
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    profile_photo_url: Optional[str] = None

class UserCreate(UserBase):
    password: str  # Plain password, will be hashed

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    profile_photo_url: Optional[str]

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
