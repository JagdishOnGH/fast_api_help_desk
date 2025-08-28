from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email (required)")
    password: str = Field(..., description="User password (required)")
