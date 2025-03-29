from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id: int = Field(foreign_key="user.id")
    
    # Relationships
    owner: "User" = Relationship(back_populates="projects")
    tables: List["Table"] = Relationship(back_populates="project")