# app/auth/oauth_service.py

import json
from typing import Optional
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import OAuthAccount, User
from app.Oauth.schemas import OAuthUserInfo
from app.users.service import UserService
from app.core.security import get_password_hash


class OAuthService:
    """Service for OAuth operations."""

    @staticmethod
    async def get_oauth_account(
        db: AsyncSession,
        provider: str,
        provider_user_id: str
    ) -> Optional[OAuthAccount]:
        """Get OAuth account by provider and provider user ID."""
        result = await db.execute(
            select(OAuthAccount).where(
                OAuthAccount.provider == provider,
                OAuthAccount.provider_user_id == provider_user_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_oauth_accounts_by_user(
        db: AsyncSession,
        user_id: int
    ) -> list[OAuthAccount]:
        """Get all OAuth accounts for a user."""
        result = await db.execute(
            select(OAuthAccount).where(OAuthAccount.user_id == user_id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def link_oauth_account(
        db: AsyncSession,
        user_id: int,
        provider: str,
        user_info: OAuthUserInfo,
        profile_data: dict
    ) -> OAuthAccount:
        """Link OAuth provider to existing user."""
        oauth_account = OAuthAccount(
            user_id=user_id,
            provider=provider,
            provider_user_id=user_info.provider_user_id,
            email=user_info.email,
            profile_data=json.dumps(profile_data)
        )
        db.add(oauth_account)
        await db.flush()
        return oauth_account

    @staticmethod
    async def create_user_from_oauth(
        db: AsyncSession,
        provider: str,
        user_info: OAuthUserInfo,
        profile_data: dict
    ) -> User:
        """Create new user from OAuth data."""
        # Generate unique username if not provided
        username = user_info.username or user_info.email.split("@")[0]
        
        # Check if username exists, make it unique
        base_username = username
        counter = 1
        while await UserService.get_by_username(db, username):
            username = f"{base_username}{counter}"
            counter += 1

        # Create user (without password)
        user = User(
            email=user_info.email,
            username=username,
            full_name=f"{user_info.first_name}  {user_info.last_name}",
            profile_picture=user_info.profile_picture,
            hashed_password=None,  # OAuth users don't have password initially
            is_active=True,
            
        )
        db.add(user)
        await db.flush()

        # Link OAuth account
        await OAuthService.link_oauth_account(
            db, user.id, provider, user_info, profile_data
        )

        return user

    @staticmethod
    async def get_or_create_oauth_user(
        db: AsyncSession,
        provider: str,
        user_info: OAuthUserInfo,
        profile_data: dict
    ) -> tuple[User, bool]:
        """
        Get existing user or create new one from OAuth.
        Returns (user, is_new) tuple.
        """
        # Check if OAuth account already exists
        oauth_account = await OAuthService.get_oauth_account(
            db, provider, user_info.provider_user_id
        )
        
        if oauth_account:
            # OAuth account exists, get the user
            user = await UserService.get_by_id(db, oauth_account.user_id)
               # ✅ FIX: Handle case where user was deleted but OAuth account remains
            if not user:
            # This shouldn't happen with CASCADE delete, but handle it anyway
            # Delete orphaned OAuth account
                await db.delete(oauth_account)
                await db.flush()
            # Continue to create new user below
            else:
                return user, False

        # Check if user with this email exists
        existing_user = await UserService.get_by_email(db, user_info.email)
        print("existing user", existing_user)
        if existing_user:
            # User exists with this email
            # Link OAuth to existing account
            await OAuthService.link_oauth_account(
                db, existing_user.id, provider, user_info, profile_data
            )
            return existing_user, False

        # Create new user
        user = await OAuthService.create_user_from_oauth(
            db, provider, user_info, profile_data
        )
        return user, True

    @staticmethod
    async def unlink_oauth_account(
        db: AsyncSession,
        user_id: int,
        provider: str
    ) -> bool:
        """Unlink OAuth provider from user."""
        result = await db.execute(
            select(OAuthAccount).where(
                OAuthAccount.user_id == user_id,
                OAuthAccount.provider == provider
            )
        )
        oauth_account = result.scalar_one_or_none()
        
        if oauth_account:
            await db.delete(oauth_account)
            return True
        return False