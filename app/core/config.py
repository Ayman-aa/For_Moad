import os
from typing import List, Optional
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dynamic Tables API"
    API_V1_STR: str = "/api"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "superuser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "aza")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dynamictables")
    DATABASE_URI: Optional[str] = None
    
    # CORS - Temporarily hardcode this to avoid .env issues
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> any:
        if isinstance(v, str):
            return v
            
        return f"postgresql+asyncpg://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
    
    class Config:
        case_sensitive = True
        # Comment out env_file for now
        # env_file = ".env"

settings = Settings()