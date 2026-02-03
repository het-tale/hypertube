# app/auth/oauth_schemas.py

from pydantic import BaseModel, EmailStr

class OAuthUserInfo(BaseModel):
    """User info from OAuth provider."""
    provider_user_id: str
    email: EmailStr
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    profile_picture: str | None = None


class OAuthCallbackResponse(BaseModel):
    """Response after successful OAuth callback."""
    message: str
    redirect_url: str