from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel

class RowBase(BaseModel):
    data: Dict[str, Any]
    
class RowCreate(RowBase):
    table_id: int
    
class RowUpdate(BaseModel):
    data: Dict[str, Any]
    
class RowRead(RowBase):
    id: int
    table_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class RowBulkCreate(BaseModel):
    rows: List[Dict[str, Any]]
    table_id: int
        
class RowBulkResponse(BaseModel):
    created: int
    errors: List[Dict[str, Any]] = []