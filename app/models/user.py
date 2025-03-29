from datetime import datetime, timezone
from typing import List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(min_length=3, max_length=50, unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="owner")