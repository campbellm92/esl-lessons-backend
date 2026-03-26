from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base schema for users
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None

# Creating users
class UserCreate(UserBase):
    password: str

# Updating users
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    password: Optional[str] = None

# Schema for responses (without password)
class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

