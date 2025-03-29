# Dynamic Tables API

A flexible FastAPI application for creating and managing dynamic data tables with customizable schemas.

## Features

- **User Authentication**: JWT-based authentication system
- **Projects Management**: Organize your data collections
- **Dynamic Tables**: Create tables with custom column schemas
- **Flexible Data Storage**: Store data with dynamic schemas using JSON fields
- **RESTful API**: Modern API design with FastAPI

## Tech Stack

- **FastAPI**: High-performance web framework
- **SQLModel**: ORM for SQLAlchemy core with Pydantic models
- **PostgreSQL**: Database with JSON field support
- **Pydantic**: Data validation with Python type annotations
- **JWT Authentication**: Secure token-based authentication

## Project Structure

```
app/
├── api/                 # API endpoints
│   ├── dependencies/    # Reusable dependencies
│   └── endpoints/       # API route handlers
├── core/                # Core functionality
│   ├── config.py        # Application configuration
│   └── security.py      # Authentication utilities
├── db/                  # Database setup
│   ├── init_db.py       # Database initialization
│   └── session.py       # Database session management
├── models/              # Database models
│   ├── project.py       # Project model
│   ├── row.py           # Dynamic row model
│   ├── table.py         # Table schema model
│   └── user.py          # User model
├── schemas/             # Pydantic schemas for API
├── services/            # Business logic layer
└── utils/               # Utility functions
    └── validators.py    # Data validation helpers
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository
   ```
   git clone https://github.com/ayman-aa/for-moad.git dynamic-tables-api
   cd dynamic-tables-api
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   source ./bin/activate .  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables
   ```
   cp .example.env .env
   # Edit .env file with your database credentials
   ```

5. Run the application
   ```
   python run.py
   ```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

The application uses the following main models:

- **User**: Authentication and user management
- **Project**: Container for organizing tables
- **Table**: Schema definition for data
- **Row**: Actual data stored in tables with dynamic schema

## Development

### Running Tests

```
pytest
```

### Code Style

This project follows PEP 8 style guidelines.

## License

[MIT License](LICENSE)

## Contributors

- [Ayman Aamam](https://github.com/ayman-aa)