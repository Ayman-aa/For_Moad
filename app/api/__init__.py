from fastapi import APIRouter
from app.api.endpoints import users

# filepath: /Ubuntu/home/ayman/For_Moad/app/app/api/__init__.py


api_router = APIRouter()

# Include user-related endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])