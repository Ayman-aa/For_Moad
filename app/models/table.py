from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON  # Import Column and JSON from SQLAlchemy
from datetime import datetime, timezone

class TableBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Table(TableBase, table=True):
    __tablename__ = "tables"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    project_id: int = Field(foreign_key="projects.id")  # Make sure this matches your Project table name
    
    # Store column definitions in JSON
    # Example: {"name": {"type": "string"}, "age": {"type": "integer"}}
    columns: Dict[str, Dict[str, Any]] = Field(
        default={}, 
        sa_column=Column(JSON)  # Use Column(JSON) here
    )
    
    # Relationships
    project: "Project" = Relationship(back_populates="tables")
    rows: List["Row"] = Relationship(back_populates="table")