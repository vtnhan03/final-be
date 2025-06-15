# FastAPI Authentication Demo

## Features
- User registration and login
- JWT-based authentication
- PIN management (set and verify)
- MySQL database storage
- Docker containerization

## Prerequisites
- Docker and Docker Compose

## Docker Setup (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo>
   cd nsfw_filter_be
   ```

2. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MySQL: localhost:3306

4. **Stop services:**
   ```bash
   docker-compose down
   ```

## Manual Setup (Alternative)

### Prerequisites
- Python 3.7+
- MySQL Server
- MySQL database created (e.g., `nsfw_filter_db`)

### Database Setup

1. **Install MySQL** (if not already installed):
   ```bash
   # macOS
   brew install mysql
   
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   
   # Windows - Download from MySQL official website
   ```

2. **Create Database:**
   ```sql
   CREATE DATABASE nsfw_filter_db;
   ```

3. **Configure Environment Variables:**
   Copy `env_example.txt` to `.env` and update with your MySQL credentials:
   ```bash
   cp env_example.txt .env
   ```

## Endpoints
- `POST /register` — Register a new user
- `POST /login` — Login and get JWT token
- `GET /me` — Get current user info (JWT required)
- `POST /set-pin` — Set a PIN for the current user (JWT required)
- `POST /verify-pin` — Verify PIN for the current user (JWT required)
- `POST /remove-pin` — Remove PIN after verification (JWT required)

## Quickstart

### With Docker (Recommended):
```bash
# Start the services
docker-compose up --build

# API will be available at http://localhost:8000
# Visit http://localhost:8000/docs for API documentation
```

### Manual Setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup MySQL database:**
   ```sql
   # Connect to MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE nsfw_filter_db;
   exit;
   ```

3. **Configure environment:**
   ```bash
   # Copy environment template
   cp env_example.txt .env
   
   # Edit .env file with your MySQL credentials
   nano .env
   ```

4. **Run the app:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Try the API:**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

## Example Usage

### Register
```json
POST /register
{
  "username": "alice",
  "password": "wonderland"
}
```

### Login
```json
POST /login (form-data: username, password)
Response: { "access_token": "...", "token_type": "bearer" }
```

### Get Current User
Set header: `Authorization: Bearer <access_token>`
```json
GET /me
Response: { "id": 1, "username": "alice", "has_pin": false }
```

### Set PIN
Set header: `Authorization: Bearer <access_token>`
```json
POST /set-pin
{
  "pin": "1234"
}
Response: { "message": "PIN set successfully" }
```

### Verify PIN
Set header: `Authorization: Bearer <access_token>`
```json
POST /verify-pin
{
  "pin": "1234"
}
Response: { "valid": true, "message": "PIN verified successfully" }
```

### Remove PIN
Set header: `Authorization: Bearer <access_token>`
```json
POST /remove-pin
{
  "current_pin": "1234"
}
Response: { "message": "PIN removed successfully" }
```

## PIN Requirements
- PIN must be 4-6 digits only
- PINs are securely hashed using bcrypt
- Each user can have their own PIN
- PIN removal requires verification of current PIN for security
- All data stored securely in MySQL database

## Environment Variables
The following environment variables can be configured:
- `MYSQL_USER` - MySQL username (default: root)
- `MYSQL_PASSWORD` - MySQL password (default: password)
- `MYSQL_HOST` - MySQL host (default: localhost)
- `MYSQL_PORT` - MySQL port (default: 3306)
- `MYSQL_DATABASE` - MySQL database name (default: nsfw_filter_db)
- `SECRET_KEY` - JWT secret key for token signing

### Docker Environment
When using Docker Compose, these variables are automatically configured:
- `MYSQL_USER`: appuser
- `MYSQL_PASSWORD`: apppassword
- `MYSQL_HOST`: mysql (container name)
- `MYSQL_DATABASE`: nsfw_filter_db

## Docker Commands

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Access MySQL directly
docker exec -it nsfw_filter_mysql mysql -u appuser -p nsfw_filter_db
```