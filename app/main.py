from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Fix imports to use absolute paths
from app.api.router import api_router
from app.core.config import settings
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB on startup
    await init_db()
    yield
    # Optional shutdown tasks go here

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Configure CORS with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)