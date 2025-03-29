from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService
from app.api.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.create(user_data, session)

@router.get("/me", response_model=UserRead)
async def read_user_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_user_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    updated_user = await UserService.update(current_user.id, user_data, session)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user