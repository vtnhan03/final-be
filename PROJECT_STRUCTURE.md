# ChildSafe API - Project Structure

This document outlines the restructured project architecture for better maintainability, scalability, and code organization.

## 📁 Project Structure

```
nsfw_filter_be/
├── app/                          # Main application package
│   ├── __init__.py              # App package initialization
│   ├── api/                     # API layer
│   │   ├── __init__.py
│   │   └── v1/                  # API version 1
│   │       ├── __init__.py
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── users.py         # User management endpoints
│   │       ├── health.py        # Health check endpoints
│   │       └── router.py        # Main API router
│   ├── auth/                    # Authentication utilities
│   │   ├── __init__.py
│   │   ├── dependencies.py      # Auth dependencies & middleware
│   │   └── google_auth.py       # Google OAuth utilities
│   ├── core/                    # Core application configuration
│   │   ├── __init__.py
│   │   └── config.py            # Settings and configuration
│   ├── db/                      # Database layer
│   │   ├── __init__.py
│   │   └── database.py          # Database connection & session
│   ├── models/                  # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   └── reset_token.py       # Reset token model
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication schemas
│   │   ├── common.py            # Common schemas
│   │   ├── pin.py               # PIN management schemas
│   │   └── user.py              # User schemas
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── email_service.py     # Email service (Resend)
│   │   ├── reset_service.py     # Password/PIN reset service
│   │   └── user_service.py      # User management service
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── jwt.py               # JWT token utilities
│       └── security.py         # Security utilities
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker compose configuration
├── Dockerfile                   # Docker container configuration
├── .env                         # Environment variables (create from env_example.txt)
├── API_DOCUMENTATION.md         # API documentation
├── environment_variables.md     # Environment setup guide
└── README.md                    # Project documentation
```

## 🏗️ Architecture Overview

### 1. **Layered Architecture**
The project follows a clean layered architecture pattern:

- **API Layer** (`app/api/`): HTTP endpoints and request/response handling
- **Service Layer** (`app/services/`): Business logic and orchestration
- **Data Layer** (`app/models/`, `app/db/`): Database models and data access
- **Auth Layer** (`app/auth/`): Authentication and authorization
- **Utils Layer** (`app/utils/`): Shared utilities and helpers

### 2. **Separation of Concerns**
Each module has a specific responsibility:

- **Models**: Database schema and ORM definitions
- **Schemas**: Request/response validation and serialization
- **Services**: Business logic and data manipulation
- **API**: HTTP endpoint definitions and routing
- **Auth**: Authentication middleware and utilities

### 3. **Dependency Injection**
FastAPI's dependency injection system is used throughout:

- Database sessions via `get_db()`
- User authentication via `get_current_user()`
- Configuration via `settings`

## 📋 Key Components

### Core Configuration (`app/core/`)
- **config.py**: Centralized configuration management using Pydantic Settings
- Environment variable handling
- Database URL construction
- CORS settings

### Database Layer (`app/db/`, `app/models/`)
- **database.py**: SQLAlchemy engine, session management, and database utilities
- **models/**: Database models with proper relationships
- Automatic table creation on startup

### Authentication (`app/auth/`)
- **dependencies.py**: JWT authentication middleware
- **google_auth.py**: Google OAuth integration
- Bearer token validation
- User session management

### Services (`app/services/`)
- **user_service.py**: User CRUD operations, authentication, PIN management
- **reset_service.py**: Password and PIN reset functionality
- **email_service.py**: Email notifications with Resend integration

### API Layer (`app/api/v1/`)
- **auth.py**: Registration, login, Google OAuth, password reset
- **users.py**: User profile, password change, PIN management
- **health.py**: Health checks and utility endpoints
- **router.py**: API route aggregation

### Utilities (`app/utils/`)
- **security.py**: Password hashing, validation, token generation
- **jwt.py**: JWT token creation and verification

## 🔧 Benefits of This Structure

### 1. **Maintainability**
- Clear separation of concerns
- Easy to locate and modify specific functionality
- Consistent code organization

### 2. **Scalability**
- Easy to add new features and endpoints
- Modular design allows independent development
- Version-based API structure (`v1`, `v2`, etc.)

### 3. **Testability**
- Services can be unit tested independently
- Mock dependencies easily
- Clear interfaces between layers

### 4. **Reusability**
- Services can be reused across different endpoints
- Utilities are shared across the application
- Schemas ensure consistent data validation

### 5. **Security**
- Centralized authentication logic
- Consistent security practices
- Easy to audit and update security measures

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Access Documentation**:
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

## 📝 Development Guidelines

### Adding New Features
1. Create models in `app/models/`
2. Define schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/v1/`
5. Update documentation

### Code Standards
- Use type hints throughout
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Use dependency injection for database sessions
- Handle errors gracefully with proper HTTP status codes

### Testing
- Write unit tests for services
- Test API endpoints with FastAPI TestClient
- Mock external dependencies (email, Google API)
- Test authentication and authorization

This restructured architecture provides a solid foundation for building and maintaining a robust, scalable FastAPI application. 