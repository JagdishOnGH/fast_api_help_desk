from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.models.user import User  # We'll need schemas for token data
from app.core import security # Import your security functions
from app.models.user import UserRole

# This tells FastAPI where the token can be obtained from.
# The "tokenUrl" should point to your login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current user from a JWT token.
    1. Decodes the JWT token.
    2. Extracts the user ID ('sub').
    3. Fetches the user from the database.
    4. Returns the user object.
    Raises HTTPException if the token is invalid or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Use the decode function from your security file
        payload = security.decode_access_token(token)
        if payload is None:
            raise credentials_exception
            
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency that relies on get_current_user and then checks
    if the user has the 'admin' role.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have admin privileges"
        )
    return current_user

def get_current_agent (
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency that relies on get_current_user and then checks
    if the user has the 'agent' role.
    """
    if current_user.role != UserRole.agent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have agent privileges"
        )
    return current_user