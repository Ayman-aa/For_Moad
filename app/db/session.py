from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URI,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    Usage:
    ```
    @.get("/items/")
    async def get_items(session: AsyncSession = Depends(get_session)):
        ...
    ```
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()