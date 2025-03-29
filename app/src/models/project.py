from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")
    
    # Relationships
    owner: "User" = Relationship(back_populates="projects")
    tables: List["Table"] = Relationship(back_populates="project")

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None