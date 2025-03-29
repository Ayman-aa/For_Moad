from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import users, projects, tables, rows
from src.db.session import create_db_and_tables

app = FastAPI(title="Dynamic Tables API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tables.router, prefix="/api/tables", tags=["tables"])
app.include_router(rows.router, prefix="/api/rows", tags=["rows"])

@app.get("/")
async def root():
    return {"message": "Welcome to Dynamic Tables API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)