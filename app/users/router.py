"""User API routes."""
from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_active_user
from app.models.models import User
from app.users.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Get current user information."""
    return current_user
