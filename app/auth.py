from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db   # ✅ instead of SessionLocal
from app.core.security import create_access_token, verify_password
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(
    
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Use form_data.username as email
    user = db.query(User).filter(User.email == form_data.username).first()

    validationResult = verify_password(form_data.password, user.password_hash)
    if not user or not validationResult:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "role":user.role}
