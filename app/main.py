

from app.routers.users import router as users_router
from app.routers.tasks import router as tasks_router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.database import Base, engine
from app.utils.exceptions import AppException
from app.utils.rate_limit import limiter
from app.routers.auth import router as auth_router




import app.models


tags_metadata = [
        {
        "name": "Authentication",
        "description": "User registration and login. Protected endpoints require a Bearer token.",
        },
        {
        "name": "Users",
        "description": "Operations involving the authenticated user's profile.",
        },
        {
        "name": "Tasks",
        "description": "Create and manage tasks belonging to the authenticated user.",
        },
    ]
app = FastAPI(
    title="AI-Ready Task Manager",
    description="""
# AI-Ready Task Manager

A production-style REST API for managing personal tasks with:

- User authentication
- JWT access tokens
- Password hashing
- Task CRUD operations
- User-owned task isolation
- Pydantic validation
- SQLAlchemy database persistence
- Rate limiting
- Background tasks
- AI-ready task suggestions

## Quick Start

1. Register with `POST /auth/register`
2. Copy the returned `access_token`
3. Click **Authorize** in Swagger UI
4. Enter `Bearer <your-token>`
5. Create and manage your tasks
""",
    version="1.0.0",
    openapi_tags=tags_metadata,
    )




app.state.limiter = limiter


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
    ):

    """Return a consistent JSON response for application exceptions."""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "detail": exc.detail,
                "status_code": exc.status_code,}
                 },
        )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(
    request: Request,
    exc: RateLimitExceeded,
    ):
    """Return a consistent response when rate limits are exceeded."""

    return JSONResponse(
        status_code=429,
        content={
            "error": {
                "type": "RateLimitExceeded",
                "detail": "Too many requests. Please try again later.",
                "status_code": 429,}
            },
        )


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Authentication"])
def root():
    """Return basic information about the API."""

    return {
        "name": "AI-Ready Task Manager",
        "version": "1.0.0",
        "docs": "/docs",
        }

