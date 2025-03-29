from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class ProjectCreate(ProjectBase):
    pass
    
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
class ProjectRead(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True