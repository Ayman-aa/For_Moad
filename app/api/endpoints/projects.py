from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.db.session import get_session
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project import ProjectService
from app.api.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await ProjectService.create(project_data, current_user.id, session)

@router.get("/", response_model=List[ProjectRead])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await ProjectService.get_all_by_user(current_user.id, session, skip, limit)

@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    project = await ProjectService.get_by_id(project_id, current_user.id, session)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    updated_project = await ProjectService.update(project_id, project_data, current_user.id, session)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    success = await ProjectService.delete(project_id, current_user.id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None