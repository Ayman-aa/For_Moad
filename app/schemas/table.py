from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel

class TableBase(BaseModel):
    name: str
    description: Optional[str] = None
    columns: Dict[str, Dict[str, Any]]
    
class TableCreate(TableBase):
    project_id: int
    
class TableUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[Dict[str, Dict[str, Any]]] = None
    
class TableRead(TableBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True