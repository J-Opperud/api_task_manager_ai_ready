from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get the current user's profile",
    )

def get_me(
    current_user: User = Depends(get_current_user),
    ):

    """Return the profile of the currently authenticated user."""

    return current_user
