from fastapi import APIRouter, Query, Request, Response, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import secrets

import httpx
from app.Oauth.schemas import OAuthUserInfo
from app.Oauth.service import OAuthService
from app.auth.router import refresh_token, set_auth_cookies
from app.auth.service import AuthService
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import create_access_token, create_refresh_token





router = APIRouter(prefix="/auth", tags=["OAuth"])


#============================================================================
# Helper Functions
# ============================================================================

def generate_state() -> str:
    """Generate secure random state for CSRF protection."""
    return secrets.token_urlsafe(32)


def get_oauth_config(provider: str) -> dict:
    """Get OAuth configuration for provider."""
    configs = {
        "42": {
            "client_id": settings.OAUTH_42_CLIENT_ID,
            "client_secret": settings.OAUTH_42_CLIENT_SECRET,
            "authorize_url": settings.OAUTH_42_AUTHORIZE_URL,
            "token_url": settings.OAUTH_42_TOKEN_URL,
            "user_info_url": settings.OAUTH_42_USER_INFO_URL,
            "redirect_uri": settings.OAUTH_42_REDIRECT_URI,
            "scope": "public",
        },
        "google": {
            "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
            "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
            "authorize_url": settings.OAUTH_GOOGLE_AUTHORIZE_URL,
            "token_url": settings.OAUTH_GOOGLE_TOKEN_URL,
            "user_info_url": settings.OAUTH_GOOGLE_USER_INFO_URL,
            "redirect_uri": settings.OAUTH_GOOGLE_REDIRECT_URI,
            "scope": "openid profile email",
        },
    }
    
    if provider not in configs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )
    
    return configs[provider]

async def exchange_code_for_token(provider: str, code: str) -> dict:
    """Exchange authorization code for access token."""
    config = get_oauth_config(provider)
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": config["redirect_uri"],
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(config["token_url"], data=data)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange code for token"
            )
        
        return response.json()

async def get_user_info_from_provider(provider: str, access_token: str) -> dict:
    """Get user info from OAuth provider."""
    config = get_oauth_config(provider)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(config["user_info_url"], headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from provider"
            )
        
        return response.json()


def normalize_user_info(provider: str, raw_data: dict) -> OAuthUserInfo:
    """Normalize user info from different providers to common format."""
    if provider == "42":
        return OAuthUserInfo(
            provider_user_id=str(raw_data["id"]),
            email=raw_data["email"],
            username=raw_data.get("login"),
            first_name=raw_data.get("first_name"),
            last_name=raw_data.get("last_name"),
            profile_picture=raw_data.get("image", {}).get("link") if "image" in raw_data else None,
        )
    
    elif provider == "google":
        return OAuthUserInfo(
            provider_user_id=raw_data["id"],
            email=raw_data["email"],
            username=raw_data.get("email", "user@example.com").split("@")[0],  # Use email prefix as username
            first_name=raw_data.get("given_name"),
            last_name=raw_data.get("family_name"),
            profile_picture=raw_data.get("picture"),
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported provider: {provider}"
        )




@router.get("/login/{provider}")
async def oauth_login(
    provider: str,
    request: Request,
    response: Response,
) -> RedirectResponse:
    """
    Initiate OAuth flow.
    
    Supports: 42, google
    """
    config = get_oauth_config(provider)
    
    # Generate state for CSRF protection
    state = generate_state()
    
    # Store state in session
    request.session["oauth_state"] = state
    request.session["oauth_provider"] = provider
    
    # Build authorization URL
    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "response_type": "code",
        "scope": config["scope"],
        "state": state,
    }
    
    auth_url = f"{config['authorize_url']}?{urlencode(params)}"
    
    return RedirectResponse(url=auth_url)



@router.get("/{provider}/callback")
async def oauth_callback(
    provider : str,
    request : Request,
    response: Response,
    code : str = Query(...),
    state : str = Query(...),
    db: AsyncSession = Depends(get_db)
) -> RedirectResponse:
    
    """
    Handle OAuth callback.
    
    This is where the provider redirects back after user approval.
    """
    # Validate state (CSRF protection)
    session_state = request.session.get("oauth_state")
    session_provider = request.session.get("oauth_provider")
    
    if not session_state or session_state != state:
        # Clear session
        request.session.clear()
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error=invalid_state",
            status_code=status.HTTP_302_FOUND
        )
    
    if session_provider != provider:
        request.session.clear()
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error=provider_mismatch",
            status_code=status.HTTP_302_FOUND
        )
    
    # Clear state from session (single use)
    del request.session["oauth_state"]
    del request.session["oauth_provider"]
    
    try:
        # Exchange code for access token
        token_data = await exchange_code_for_token(provider, code)
        access_token = token_data["access_token"]
        
        # Get user info from provider
        raw_user_data = await get_user_info_from_provider(provider, access_token)
        print("raw data", raw_user_data)
        # Normalize user info
        user_info = normalize_user_info(provider, raw_user_data)
        
        # Get or create user
        user, is_new = await OAuthService.get_or_create_oauth_user(
            db, provider, user_info, raw_user_data
        )
        
        if not user.is_active:
            return RedirectResponse(
                url=f"{settings.FRONTEND_URL}/login?error=inactive_user",
                status_code=status.HTTP_302_FOUND
            )
        
        # Create JWT tokens
        jwt_access_token = create_access_token({"sub": str(user.id)})
        jwt_refresh_token = create_refresh_token({"sub": str(user.id)})
        
        # Store refresh token in database
        await AuthService.create_refresh_token_record(db, user.id, jwt_refresh_token)
        
        await db.commit()

        print("access_toke", jwt_access_token)
        print("refesh", jwt_refresh_token)
        # Set cookies
        
        # Redirect to frontend
        redirect_url = f"{settings.FRONTEND_URL}/home"
        if is_new:
            redirect_url += "?welcome=true"
        
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        set_auth_cookies(response, jwt_access_token, jwt_refresh_token)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error here
        print(f"OAuth error: {str(e)}")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/login?error=oauth_failed",
            status_code=status.HTTP_302_FOUND
        )