"""User Pydantic schemas using v2."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str | None = None
    profile_picture : str | None = None
    username : str | None = None
    preferred_language : str = "en"



class UserCreate(UserBase):
    """Schema for user creation."""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user update."""

    email: EmailStr | None = None
    full_name: str | None = None
    # password: str | None = Field(None, min_length=8, max_length=100)
    username: str | None = None
    preferred_language: str | None = None
    bio : str | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    bio : str | None = None
    email_verified : bool
    


class UserInDB(UserResponse):
    """Schema for user in database (includes hashed password)."""

    hashed_password: str


class PasswordUpdate(BaseModel):
    """Schema for password update."""

    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
