"""
Database initialization and session management.
"""
from app.db.session import get_session
from app.db.init_db import init_db

__all__ = ["get_session", "init_db"]