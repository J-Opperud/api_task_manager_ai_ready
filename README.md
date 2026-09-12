Task Manager API

## overveiw

A production-ready FastAPI task management API with JWT authentication, SQLAlchemy database persistence, validation, protected task CRUD operations, background activity logging, automated testing, and an AI-ready suggestion endpoint.

## Features

- JWT-based user authentication
- Secure bcrypt password hashing
- User profile endpoint
- Protected task CRUD operations
- Task filtering and pagination
- User-level task isolation
- Pydantic request and response validation
- Consistent custom error responses
- Background activity logging
- AI-ready task suggestion endpoint
- Automatic Swagger/OpenAPI documentation
- Pytest test suite with isolated test database
- CORS configured for the frontend
- Tech Stack
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT
- bcrypt
- Pytest


## Project Structure


task-manager/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── task.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── users.py
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py
│       ├── notifications.py
│       ├── rate_limit.py
│       └── security.py
├── tests/
│   ├── conftest.py
│   └── test_task.py
├── log/
├── .env
├── requirements.txt
└── README.md

Setup
1. Create a virtual environment
python -m venv venv

2. Activate the virtual environment

Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file containing the application's configuration and JWT secret.

Keep secrets out of source control.

5. Start the development server

uvicorn app.main:app --reload


The API will be available at:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation.

Documentation	URL
Swagger UI	http://127.0.0.1:8000/docs
ReDoc	http://127.0.0.1:8000/redoc

## Application

- App-level metadata
- Endpoint descriptions
- Request validation
- Response schemas
- Endpoint docstrings
- Interactive Swagger testing
- API version information
- Endpoint tags and descriptions
- Authentication
- Register
- POST /auth/register


Creates a new user with a securely hashed password and returns a JWT access token.

Login
POST /auth/login


Validates the user's credentials and returns a JWT access token.

Protected endpoints require the token in the request header:

Authorization: Bearer <token>

Current User
GET /users/me


Returns the profile of the authenticated user.

Passwords are hashed before being stored and are never returned through any response schema.

## Task API

All task endpoints require authentication.

Method Endpoint	Description
POST /tasks	       Create a task
GET	/tasks	       List the authenticated user's tasks
GET	/tasks/{id}   Get a specific task
PATCH /tasks/{id}    Partially update a task
DELETE /tasks/{id}   Delete a task
POST /tasks/{id}/    suggest Generate an AI-ready suggestion




- The task list supports optional query parameters:

    completed
    priority
    skip
    limit

Example:

GET /tasks?priority=high&completed=false&skip=0&limit=10


Users can only access tasks belonging to their own account.

Attempting to access another user's task returns a 403 Forbidden response.

## Data Models

 Model Archetcture 

User
├── id
├── name
├── email
├── hashed_password
├── is_active
├── created_at
└── tasks → relationship


User
Field	              Description
id	              Unique user ID
name	              User's name
email	              Unique email address
hashed_password	Securely hashed password
is_active	       Account status
created_at	       Account creation timestamp


Task
├── id
├── title
├── description
├── priority
├── completed
├── user_id → FK(users.id)
├── created_at
└── updated_at

Task
Field	       Description
id	       Unique task ID
title	       Task title, 1–200 characters
description	Optional description, up to 2000 characters
priority	Task priority enum
completed	Completion status
user_id	Owning user's ID
created_at	Creation timestamp
updated_at	Last update timestamp


Importent relationship

users.id
   ↑
   │ ForeignKey
   │
tasks.user_id


Pydantic schemas enforce field constraints and validate incoming data before it reaches the database.

Create, update, and response schemas are separated to keep request and response responsibilities clear.

Response schemas use from_attributes = True.

## Error Handling

The application uses custom exceptions for common API errors:

NotFoundException
DuplicateException
ForbiddenException

Global exception handlers return errors using a consistent JSON response format.

Example:

{
  "error": {
    "type": "NotFoundException",
    "detail": "Task with id 9999 not found",
    "status_code": 404
  }
}


Unauthorized users receive 401 responses.

Authenticated users attempting to access another user's task receive 403 responses.

Invalid request data is handled through Pydantic validation and returns 422 responses.

## Background Tasks

The application uses FastAPI background tasks for activity logging.

Task activity is recorded without blocking the API response.

Example log files:

log/
├── activity_log.txt
└── calendar_log.txt


The background functionality provides a foundation for additional tasks such as notifications, reports, or other asynchronous processing.

## AI-Ready Endpoint

The project includes a placeholder endpoint designed for future AI integration:

POST /tasks/{id}/suggest


The endpoint accepts the authenticated user's task ID, retrieves the task description, and returns a placeholder suggestion.

Example response:

{
  "suggestion": "Break this task into smaller steps and prioritize the most important action first."
}


The endpoint is intentionally structured so a real AI model can be connected later without changing the core task-management functionality.

## Security
              config.py
                    │
              SECRET_KEY
              ALGORITHM
              TOKEN EXPIRY
                    │
                    ▼
              security.py
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
 hash_password  verify_password  create_access_token
                                  │
                                  ▼
                              JWT + exp
                                  │
                                  ▼
                         get_current_user
                                  │
                                  ▼
                               User

- The API includes:

       JWT authentication
       JWT token expiration
       bcrypt password hashing
       Protected task endpoints
       User-level authorization
       Pydantic input validation
       Environment-based configuration
       CORS configured for localhost:8501

Secrets should be stored in .env and should never be committed to source control.

## Testing

The project uses pytest and FastAPI's TestClient.

Run the complete test suite:

pytest -v


Run tests with coverage:

pytest --cov=app --cov-report=term-missing

Current Test Results
24 passed

Current Coverage
Name                         Stmts   Miss  Cover
------------------------------------------------
app\__init__.py                  0      0   100%
app\config.py                    7      0   100%
app\database.py                 10      2    80%
app\main.py                     28      2    93%
app\models\task.py              21      0   100%
app\models\user.py              13      0   100%
app\routers\auth.py             35      8    77%
app\routers\tasks.py            63      1    98%
app\routers\users.py             8      0   100%
app\schemas\auth.py             10      0   100%
app\schemas\task.py             16      0   100%
app\schemas\user.py              4      0   100%
app\utils\exceptions.py         20      2    90%
app\utils\notifications.py      12      0   100%
app\utils\rate_limit.py          3      0   100%
app\utils\security.py           36      6    83%
------------------------------------------------
TOTAL                          289     21    93%


- The test suite covers:

    Task creation
    Task listing
    Task filtering
    Pagination
    Pagination validation
    Task retrieval
    Missing tasks
    Task updates
    Task deletion
    Authentication requirements
    User authorization
    Current user profile
    Invalid login credentials
    AI suggestion endpoint
    AI suggestion authorization
    AI suggestion not-found handling
    Development Commands
    Start the API

## Run tests

pytest -v

## Run coverage

pytest --cov=app --cov-report=term-missing

## API Workflow



1. Register a user
       ↓
2. Receive JWT token
       ↓
3. Authenticate requests with Bearer token
       ↓
4. Create and manage tasks
       ↓
5. Request AI-ready suggestions

Project Goals

This project demonstrates a complete FastAPI application with:

User authentication
Database persistence
Password security
Input validation
Authorization and user isolation
CRUD operations
Custom exception handling
Background processing
Automated testing
API documentation
Test coverage
A foundation for future AI integration

The AI suggestion endpoint provides the starting point for extending the application with an actual AI model in future modules.
