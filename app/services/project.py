from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    @staticmethod
    async def get_by_id(project_id: int, user_id: int, session: AsyncSession) -> Optional[Project]:
        """Get a project by id that belongs to the user"""
        result = await session.exec(
            select(Project).where(Project.id == project_id, Project.user_id == user_id)
        )
        return result.first()

    @staticmethod
    async def get_all_by_user(user_id: int, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects belonging to a user"""
        result = await session.exec(
            select(Project)
            .where(Project.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.all()

    @staticmethod
    async def create(project_data: ProjectCreate, user_id: int, session: AsyncSession) -> Project:
        """Create a new project"""
        db_project = Project(
            **project_data.dict(),
            user_id=user_id
        )
        
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project

    @staticmethod
    async def update(
        project_id: int, 
        project_data: ProjectUpdate, 
        user_id: int, 
        session: AsyncSession
    ) -> Optional[Project]:
        """Update a project"""
        db_project = await ProjectService.get_by_id(project_id, user_id, session)
        if not db_project:
            return None
            
        update_data = project_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
            
        await session.commit()
        await session.refresh(db_project)
        return db_project

    @staticmethod
    async def delete(project_id: int, user_id: int, session: AsyncSession) -> bool:
        """Delete a project"""
        db_project = await ProjectService.get_by_id(project_id, user_id, session)
        if not db_project:
            return False
            
        await session.delete(db_project)
        await session.commit()
        return True