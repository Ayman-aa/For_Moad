from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.table import TableCreate, TableRead, TableUpdate
from app.services.table import TableService

router = APIRouter()

@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(
    table_data: TableCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await TableService.create(table_data, current_user.id, session)

@router.get("/project/{project_id}", response_model=List[TableRead])
async def read_tables_by_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await TableService.get_all_by_project(project_id, current_user.id, session)

@router.get("/{table_id}", response_model=TableRead)
async def read_table(
    table_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    table = await TableService.check_user_access(table_id, current_user.id, session)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.patch("/{table_id}", response_model=TableRead)
async def update_table(
    table_id: int,
    table_data: TableUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    updated_table = await TableService.update(table_id, table_data, current_user.id, session)
    if not updated_table:
        raise HTTPException(status_code=404, detail="Table not found")
    return updated_table

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    success = await TableService.delete(table_id, current_user.id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")