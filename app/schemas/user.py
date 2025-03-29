from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str