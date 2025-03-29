from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.row import RowCreate, RowRead, RowUpdate, RowBulkCreate, RowBulkResponse
from app.services.row import RowService

router = APIRouter()

@router.post("/", response_model=RowRead, status_code=status.HTTP_201_CREATED)
async def create_row(
    row_data: RowCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await RowService.create(row_data, current_user.id, session)

@router.post("/bulk", response_model=RowBulkResponse, status_code=status.HTTP_201_CREATED)
async def create_rows_bulk(
    bulk_data: RowBulkCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await RowService.bulk_create(bulk_data, current_user.id, session)

@router.get("/table/{table_id}", response_model=List[RowRead])
async def read_rows_by_table(
    table_id: int,
    skip: int = 0,
    limit: int = Query(default=100, lte=1000),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await RowService.get_all_by_table(table_id, current_user.id, session, skip, limit)

@router.get("/{row_id}", response_model=RowRead)
async def read_row(
    row_id: int,
    table_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    row = await RowService.get_by_id(row_id, table_id, current_user.id, session)
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    return row

@router.patch("/{row_id}", response_model=RowRead)
async def update_row(
    row_id: int,
    row_data: RowUpdate,
    table_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    updated_row = await RowService.update(row_id, row_data, table_id, current_user.id, session)
    if not updated_row:
        raise HTTPException(status_code=404, detail="Row not found")
    return updated_row

@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_row(
    row_id: int,
    table_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    success = await RowService.delete(row_id, table_id, current_user.id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Row not found")