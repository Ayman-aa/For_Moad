from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON  # Import Column and JSON from SQLAlchemy
from datetime import datetime, timezone

class RowBase(SQLModel):
    # Data is stored as JSON, corresponding to the columns defined in the table
    # You need to use sa_column=Column(JSON) to specify JSON type
    data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

class Row(RowBase, table=True):
    __tablename__ = "rows"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    table_id: int = Field(foreign_key="tables.id")  # Make sure this matches your Table table name
    
    # Relationship
    table: "Table" = Relationship(back_populates="rows")