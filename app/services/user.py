from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    async def get_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
        """Get a user by id"""
        user = await session.get(User, user_id)
        return user

    @staticmethod
    async def get_by_email(email: str, session: AsyncSession) -> Optional[User]:
        """Get a user by email"""
        result = await session.exec(select(User).where(User.email == email))
        return result.first()

    @staticmethod
    async def create(user_data: UserCreate, session: AsyncSession) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = await UserService.get_by_email(user_data.email, session)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        # Create user with hashed password
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password)
        )
        
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def update(user_id: int, user_data: UserUpdate, session: AsyncSession) -> Optional[User]:
        """Update user information"""
        db_user = await UserService.get_by_id(user_id, session)
        if not db_user:
            return None
            
        # Update user data
        user_data_dict = user_data.dict(exclude_unset=True)
        
        # Hash password if it exists
        if "password" in user_data_dict:
            user_data_dict["hashed_password"] = get_password_hash(user_data_dict.pop("password"))
            
        # Update user attributes
        for key, value in user_data_dict.items():
            setattr(db_user, key, value)
            
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def authenticate(email: str, password: str, session: AsyncSession) -> Optional[User]:
        """Authenticate a user"""
        user = await UserService.get_by_email(email, session)
        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
            
        return user