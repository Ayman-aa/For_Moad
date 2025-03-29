from sqlmodel import SQLModel

from app.db.session import engine
from app.models.user import User
from app.models.project import Project
from app.models.table import Table
from app.models.row import Row

async def init_db() -> None:
    """
    Initialize database tables if they don't exist.
    This should be called on app startup.
    """
    async with engine.begin() as conn:
        # Create all tables that don't exist
        await conn.run_sync(SQLModel.metadata.create_all)