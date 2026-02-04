"""User API routes."""
import re

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.models import User
from app.users.dependencies import UserUpdateForm, validate_profile_picture
from app.users.expection import EmailAlreadyInUse, UserNotFoundException, UsernameAlreadyInUse
from app.users.schemas import UserResponse, UserUpdate
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Get current user information."""
    return current_user



@router.put("/me", response_model=UserResponse)
async def update_current_user_info(
    form_data: UserUpdateForm = Depends(),  # Much cleaner!
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_db),
) -> User:
    """Update current user information and profile picture."""
    print("Received form data:", form_data)
    # Validate profile picture
    if form_data.profile_picture:
        await validate_profile_picture(form_data.profile_picture)
    
    # Convert to Pydantic schema
    update_data = form_data.to_pydantic()
    
    try:
        updated_user = await UserService.update_user_info(
            db=db,
            user_id=current_user.id,
            updated_data=update_data,
            profile_picture=form_data.profile_picture
        )
        return updated_user
        
    except EmailAlreadyInUse as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UsernameAlreadyInUse as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

