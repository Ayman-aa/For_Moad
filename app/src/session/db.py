from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.config import settings

# Create async PostgreSQL engine
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_db_and_tables():
    async with engine.begin() as conn:
        # Create tables that don't exist yet
        await conn.run_sync(SQLModel.metadata.create_all)