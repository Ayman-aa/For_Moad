from typing import Optional, List, Dict, Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.table import Table
from app.models.project import Project
from app.schemas.table import TableCreate, TableUpdate
from app.utils.validators import validate_column_schema

class TableService:
    @staticmethod
    async def get_by_id(table_id: int, session: AsyncSession) -> Optional[Table]:
        """Get a table by id"""
        result = await session.exec(select(Table).where(Table.id == table_id))
        return result.first()

    @staticmethod
    async def check_user_access(table_id: int, user_id: int, session: AsyncSession) -> Optional[Table]:
        """Check if a user has access to a table and return the table if they do"""
        result = await session.exec(
            select(Table)
            .join(Project)
            .where(Table.id == table_id, Project.user_id == user_id)
        )
        return result.first()

    @staticmethod
    async def get_all_by_project(project_id: int, user_id: int, session: AsyncSession) -> List[Table]:
        """Get all tables in a project"""
        result = await session.exec(
            select(Table)
            .join(Project)
            .where(Table.project_id == project_id, Project.user_id == user_id)
        )
        return result.all()

    @staticmethod
    async def create(table_data: TableCreate, user_id: int, session: AsyncSession) -> Table:
        """Create a new table"""
        # Verify the project exists and belongs to user
        result = await session.exec(
            select(Project).where(
                Project.id == table_data.project_id,
                Project.user_id == user_id
            )
        )
        project = result.first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you don't have access"
            )
            
        # Validate column schema
        if not validate_column_schema(table_data.columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid column schema format"
            )
            
        # Create table
        db_table = Table(**table_data.dict())
        
        session.add(db_table)
        await session.commit()
        await session.refresh(db_table)
        return db_table

    @staticmethod
    async def update(
        table_id: int, 
        table_data: TableUpdate, 
        user_id: int, 
        session: AsyncSession
    ) -> Optional[Table]:
        """Update a table"""
        # Check access
        db_table = await TableService.check_user_access(table_id, user_id, session)
        if not db_table:
            return None
            
        # Validate column schema if it's being updated
        update_data = table_data.dict(exclude_unset=True)
        if "columns" in update_data and not validate_column_schema(update_data["columns"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid column schema format"
            )
            
        # Update table
        for key, value in update_data.items():
            setattr(db_table, key, value)
            
        await session.commit()
        await session.refresh(db_table)
        return db_table

    @staticmethod
    async def delete(table_id: int, user_id: int, session: AsyncSession) -> bool:
        """Delete a table"""
        # Check access
        db_table = await TableService.check_user_access(table_id, user_id, session)
        if not db_table:
            return False
            
        await session.delete(db_table)
        await session.commit()
        return True