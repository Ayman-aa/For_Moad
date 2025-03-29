from datetime import datetime
from typing import Dict, List, Optional

from sqlmodel import Field, JSON, Relationship, SQLModel

class TableBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Table(TableBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    project_id: int = Field(foreign_key="project.id")
    
    # Store column definitions in JSON
    # Example: {"name": {"type": "string"}, "age": {"type": "integer"}}
    columns: Dict = Field(default={}, sa_column=JSON)
    
    # Relationships
    project: "Project" = Relationship(back_populates="tables")
    rows: List["Row"] = Relationship(back_populates="table")

class TableCreate(TableBase):
    columns: Dict
    project_id: int

class TableRead(TableBase):
    id: int
    columns: Dict
    created_at: datetime
    updated_at: datetime
    project_id: int

class TableUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    columns: Optional[Dict] = None