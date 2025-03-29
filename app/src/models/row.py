from datetime import datetime
from typing import Dict, Optional

from sqlmodel import Field, JSON, Relationship, SQLModel

class RowBase(SQLModel):
    # Data is stored as JSON, corresponding to the columns defined in the table
    data: Dict = Field(sa_column=JSON)

class Row(RowBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    table_id: int = Field(foreign_key="table.id")
    
    # Relationship
    table: "Table" = Relationship(back_populates="rows")

class RowCreate(RowBase):
    table_id: int

class RowRead(RowBase):
    id: int
    created_at: datetime
    updated_at: datetime
    table_id: int

class RowUpdate(SQLModel):
    data: Optional[Dict] = None