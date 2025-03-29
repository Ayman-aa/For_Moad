import os
import sys

# Add parent directory to path so Python can find your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app from the app directory
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)