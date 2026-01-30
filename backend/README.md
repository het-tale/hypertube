# FastAPI Authentication Template

A production-ready FastAPI project implementing secure cookie-based authentication using JWT access and refresh tokens with refresh rotation. This template provides a clean, modular structure following security best practices.

## 🎯 Features

- **Secure Cookie-Based Authentication**: HttpOnly, Secure, SameSite cookies
- **JWT Tokens**: Separate access and refresh tokens
- **Refresh Token Rotation**: Stateful refresh tokens with automatic rotation
- **PostgreSQL with Async Support**: Using SQLAlchemy async and asyncpg
- **Pydantic v2**: For data validation and settings management
- **Argon2 Password Hashing**: Industry-standard password hashing
- **Alembic Migrations**: Database schema version control
- **Modular Architecture**: Clean separation of concerns (auth, users, core, db)
- **Security Best Practices**: Input validation, SQL injection prevention, CORS configuration

## 📁 Project Structure

```
fastApi-temp/
├── alembic/                  # Database migrations
│   ├── versions/             # Migration files
│   ├── env.py               # Alembic environment
│   └── script.py.mako       # Migration template
├── app/
│   ├── auth/                # Authentication module
│   │   ├── __init__.py
│   │   ├── dependencies.py  # Auth dependencies
│   │   ├── router.py        # Auth endpoints
│   │   ├── schemas.py       # Auth Pydantic models
│   │   └── service.py       # Auth business logic
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py        # Settings with Pydantic
│   │   └── security.py      # Security utilities
│   ├── db/                  # Database configuration
│   │   ├── __init__.py
│   │   └── session.py       # Database session
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── models.py        # SQLAlchemy models
│   ├── users/               # Users module
│   │   ├── __init__.py
│   │   ├── router.py        # User endpoints
│   │   ├── schemas.py       # User Pydantic models
│   │   └── service.py       # User business logic
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── .env.example             # Environment variables template
├── .gitignore
├── alembic.ini              # Alembic configuration
├── docker-compose.yml       # PostgreSQL container
├── pyproject.toml           # Project dependencies
├── README.md
└── requirements.txt         # Alternative dependency file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL (or use Docker Compose)
- pip or uv for package management

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastApi-temp
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and update the values:

   - Generate a secure `SECRET_KEY` (at least 32 characters)
   - Update `DATABASE_URL` if needed
   - Set `COOKIE_SECURE=True` in production
   - Configure `ALLOWED_ORIGINS` for your frontend

5. **Start PostgreSQL**

   ```bash
   docker-compose up -d
   ```

6. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 API Endpoints

### Authentication

#### Register

```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

#### Login

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response includes HttpOnly cookies:

- `access_token`: Short-lived JWT (15 minutes)
- `refresh_token`: Long-lived JWT (7 days)

#### Refresh Token

```bash
POST /auth/refresh
```

Automatically rotates the refresh token (revokes old, creates new).

#### Logout

```bash
POST /auth/logout
```

Revokes the current refresh token and clears cookies.

#### Logout from All Devices

```bash
POST /auth/logout-all
```

Revokes all refresh tokens for the user.

### Users

#### Get Current User

```bash
GET /users/me
```

Returns the authenticated user's information.

## 🔒 Security Features

### Cookie Security

- **HttpOnly**: Prevents JavaScript access to tokens
- **Secure**: Cookies only sent over HTTPS (configurable)
- **SameSite**: CSRF protection (lax/strict/none)
- **Domain**: Configurable cookie domain

### Token Security

- **Access Token**: Short-lived (15 minutes by default)
- **Refresh Token**: Long-lived (7 days by default)
- **Stateful Refresh Tokens**: Stored in database with revocation support
- **Token Rotation**: Old refresh token revoked when new one issued
- **Automatic Cleanup**: Expired tokens can be cleaned up

### Password Security

- **Argon2**: Memory-hard hashing algorithm
- **Configurable Parameters**: Memory cost, time cost, parallelism
- **Validation**: Minimum length requirements

### Database Security

- **Async SQLAlchemy**: Prevents SQL injection
- **Input Validation**: Pydantic v2 models
- **Parameterized Queries**: Built-in with ORM

## 🛠️ Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history
```

## 🧪 Testing

Example requests using curl:

### Register a user

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }' \
  -c cookies.txt
```

### Get current user (using cookies)

```bash
curl -X GET http://localhost:8000/users/me \
  -b cookies.txt
```

### Refresh token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -b cookies.txt \
  -c cookies.txt
```

### Logout

```bash
curl -X POST http://localhost:8000/auth/logout \
  -b cookies.txt
```

## ⚙️ Configuration

All configuration is done through environment variables in `.env`:

| Variable                      | Description                    | Default               |
| ----------------------------- | ------------------------------ | --------------------- |
| `DATABASE_URL`                | PostgreSQL connection string   | Required              |
| `SECRET_KEY`                  | JWT secret key (32+ chars)     | Required              |
| `ALGORITHM`                   | JWT algorithm                  | HS256                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime          | 15                    |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | Refresh token lifetime         | 7                     |
| `APP_NAME`                    | Application name               | FastAPI Auth Template |
| `DEBUG`                       | Debug mode                     | False                 |
| `ALLOWED_ORIGINS`             | CORS origins (comma-separated) | localhost             |
| `COOKIE_SECURE`               | Use secure cookies (HTTPS)     | True                  |
| `COOKIE_SAMESITE`             | SameSite policy                | lax                   |
| `COOKIE_DOMAIN`               | Cookie domain                  | None                  |

## 🏭 Production Deployment

### Important Security Settings

1. **Generate a strong SECRET_KEY**

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable secure cookies**

   ```bash
   COOKIE_SECURE=True
   ```

3. **Configure CORS properly**

   ```bash
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

4. **Use HTTPS**

   - Deploy behind a reverse proxy (nginx, traefik)
   - Enable TLS/SSL certificates

5. **Set DEBUG=False**
   ```bash
   DEBUG=False
   ```

### Running with Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or using gunicorn:

```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Customization

### Adding New Endpoints

1. Create a new router in the appropriate module
2. Add business logic to the service layer
3. Define Pydantic schemas for validation
4. Include the router in `app/main.py`

### Adding Database Models

1. Create model in `app/models/models.py`
2. Generate migration: `alembic revision --autogenerate -m "Add new model"`
3. Apply migration: `alembic upgrade head`

### Extending User Model

Add fields to the `User` model in `app/models/models.py` and create a migration.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is provided as a template for building FastAPI applications with authentication.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for the robust ORM
- Pydantic for data validation
- Alembic for database migrations
- Argon2 for secure password hashing
