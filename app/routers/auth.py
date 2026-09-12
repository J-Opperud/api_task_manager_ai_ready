from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.utils.exceptions import DuplicateException, UnauthorizedException
from app.utils.rate_limit import limiter

from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
    )


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Register a new user",
    responses={
        201: {"description": "User registered successfully."},
        409: {"description": "Email or username already exists."},
        422: {"description": "Validation error"},
        },
    )
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    ):
    """Register a new user and return a JWT access token."""

    existing = db.query(User).filter(
        (User.email == request.email) |
        (User.name == request.name)
        ).first()

    if existing:
        raise DuplicateException(
            "User",
            "email or name",
            request.email,
            )

    user = User(
        name=request.name,
        email=request.email,
        hashed_password=hash_password(request.password),
        )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateException(
            "User",
            "email or name",
            request.email,
            )

    db.refresh(user)

    token = create_access_token(
        data={"sub": str(user.id)}
        )

    return {
        "access_token": token,
        "token_type": "bearer",
        }


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in a user",
    responses={
        200: {"description": "Login successful."},
        401: {"description": "Invalid email or password."},
        422: {"description": "Validation error"},
        },
    )
@limiter.limit("5/minute")
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db),

    ):

    """Authenticate a user and return a JWT access token."""

    user = db.query(User).filter(
        User.email == login_data.email
        ).first()

    if not user or not verify_password(
        login_data.password,
        user.hashed_password,
        ):

        raise UnauthorizedException(
            "Invalid email or password"
            )

    if not user.is_active:
        raise UnauthorizedException(
            "User account is inactive"
            )

    token = create_access_token(
        data={"sub": str(user.id)}
        )

    return {
        "access_token": token,
        "token_type": "bearer",
        }
