# dependencies/form_schemas.py
from fastapi import Form, HTTPException, UploadFile, File, status
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr

from app.users.schemas import UserUpdate


class UserUpdateForm:
    """Dependency to parse multipart form data into structured data."""
    
    def __init__(
        self,
        email: Optional[str] = Form(None),
        full_name: Optional[str] = Form(None),
        username: Optional[str] = Form(None),
        preferred_language: Optional[str] = Form(None),
        bio: Optional[str] = Form(None),
        profile_picture: Optional[UploadFile] = File(None),
    ):
        self.email = email
        self.full_name = full_name
        self.username = username
        self.preferred_language = preferred_language
        self.bio = bio
        self.profile_picture = profile_picture
    
    def to_pydantic(self) -> "UserUpdate":
        """Convert to Pydantic model."""

        return UserUpdate(
            email=self.email,
            full_name=self.full_name,
            username=self.username,
            preferred_language=self.preferred_language,
            bio=self.bio
        )
    

async def parse_user_update_form(
    email: Annotated[Optional[str], Form(None)] = None,
    full_name: Annotated[Optional[str], Form(None)] = None,
    username: Annotated[Optional[str], Form(None)] = None,
    preferred_language: Annotated[Optional[str], Form(None)] = None,
    bio: Annotated[Optional[str], Form(None)] = None,
) -> UserUpdate:
    """Parse and validate user update form data."""
    try:
        return UserUpdate(
            email=email,
            full_name=full_name,
            username=username,
            preferred_language=preferred_language,
            bio=bio
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


async def validate_profile_picture(
    profile_picture: Annotated[Optional[UploadFile], File(None)] = None,
) -> Optional[UploadFile]:
    """Validate profile picture file."""
    if not profile_picture:
        return None
    
    # Check file size (800KB = 800,000 bytes)
    contents = await profile_picture.read()
    if len(contents) > 800_000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile picture must be less than 800KB"
        )
    
    # Check file type
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if profile_picture.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile picture must be JPG, PNG, or GIF"
        )
    
    # Reset file pointer for later use
    await profile_picture.seek(0)
    
    return profile_picture