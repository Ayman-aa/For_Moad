from fastapi import APIRouter

from app.api.endpoints import users, auth, projects, tables, rows

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(tables.router, prefix="/tables", tags=["tables"])
api_router.include_router(rows.router, prefix="/rows", tags=["rows"])