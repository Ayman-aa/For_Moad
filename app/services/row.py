from typing import Optional, List, Dict, Any
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.row import Row
from app.models.table import Table
from app.models.project import Project
from app.schemas.row import RowCreate, RowUpdate, RowBulkCreate, RowBulkResponse
from app.utils.validators import validate_row_data

class RowService:
    @staticmethod
    async def get_table_with_access(table_id: int, user_id: int, session: AsyncSession) -> Optional[Table]:
        """Get a table if the user has access to it"""
        result = await session.exec(
            select(Table)
            .join(Project)
            .where(Table.id == table_id, Project.user_id == user_id)
        )
        return result.first()

    @staticmethod
    async def get_by_id(row_id: int, table_id: int, user_id: int, session: AsyncSession) -> Optional[Row]:
        """Get a row by id if the user has access to its table"""
        # First check table access
        table = await RowService.get_table_with_access(table_id, user_id, session)
        if not table:
            return None
            
        # Get the row
        row = await session.get(Row, row_id)
        if row and row.table_id == table_id:
            return row
        return None

    @staticmethod
    async def get_all_by_table(
        table_id: int, 
        user_id: int, 
        session: AsyncSession,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Row]:
        """Get all rows in a table"""
        # Check table access
        table = await RowService.get_table_with_access(table_id, user_id, session)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found or you don't have access"
            )
            
        # Get rows with pagination
        result = await session.exec(
            select(Row)
            .where(Row.table_id == table_id)
            .offset(skip)
            .limit(limit)
        )
        return result.all()

    @staticmethod
    async def create(row_data: RowCreate, user_id: int, session: AsyncSession) -> Row:
        """Create a new row"""
        # Get the table with schema
        table = await RowService.get_table_with_access(row_data.table_id, user_id, session)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found or you don't have access"
            )
            
        # Validate row data against table schema
        validation_errors = validate_row_data(row_data.data, table.columns)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid row data: {validation_errors}"
            )
            
        # Create row
        db_row = Row(
            data=row_data.data,
            table_id=row_data.table_id
        )
        
        session.add(db_row)
        await session.commit()
        await session.refresh(db_row)
        return db_row
        
    @staticmethod
    async def bulk_create(bulk_data: RowBulkCreate, user_id: int, session: AsyncSession) -> RowBulkResponse:
        """Create multiple rows at once"""
        # Get the table with schema
        table = await RowService.get_table_with_access(bulk_data.table_id, user_id, session)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Table not found or you don't have access"
            )
        
        response = RowBulkResponse(created=0)
        
        # Process each row
        for i, row_data in enumerate(bulk_data.rows):
            # Validate row
            validation_errors = validate_row_data(row_data, table.columns)
            if validation_errors:
                response.errors.append({
                    "row_index": i,
                    "data": row_data,
                    "errors": validation_errors
                })
                continue
                
            # Create valid row
            db_row = Row(
                data=row_data,
                table_id=bulk_data.table_id
            )
            session.add(db_row)
            response.created += 1
            
        # Commit all valid rows
        if response.created > 0:
            await session.commit()
            
        return response

    @staticmethod
    async def update(
        row_id: int, 
        row_data: RowUpdate, 
        table_id: int, 
        user_id: int, 
        session: AsyncSession
    ) -> Optional[Row]:
        """Update a row"""
        # Get row with access check
        db_row = await RowService.get_by_id(row_id, table_id, user_id, session)
        if not db_row:
            return None
            
        # Get table for schema validation
        table = await session.get(Table, table_id)
        
        # Validate updated data against table schema
        validation_errors = validate_row_data(row_data.data, table.columns)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid row data: {validation_errors}"
            )
            
        # Update row
        db_row.data = row_data.data
        
        await session.commit()
        await session.refresh(db_row)
        return db_row

    @staticmethod
    async def delete(row_id: int, table_id: int, user_id: int, session: AsyncSession) -> bool:
        """Delete a row"""
        # Get row with access check
        db_row = await RowService.get_by_id(row_id, table_id, user_id, session)
        if not db_row:
            return False
            
        await session.delete(db_row)
        await session.commit()
        return True