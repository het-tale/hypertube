"""Authentication service layer."""
from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_refresh_token, utcnow
from app.models.models import RefreshToken, User


class AuthService:
    """Service layer for authentication operations."""

    @staticmethod
    async def create_refresh_token_record(
        db: AsyncSession, user_id: int, token: str
    ) -> RefreshToken:
        """Create a new refresh token record in database."""
        expires_at = utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        db.add(db_token)
        await db.flush()
        await db.refresh(db_token)
        return db_token

    @staticmethod
    async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
        """Get refresh token record from database."""
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token, RefreshToken.is_revoked.is_(False)
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def revoke_refresh_token(db: AsyncSession, token: RefreshToken) -> None:
        """Revoke a refresh token."""
        token.is_revoked = True
        token.revoked_at = utcnow()
        await db.flush()

    @staticmethod
    async def revoke_all_user_tokens(db: AsyncSession, user_id: int) -> None:
        """Revoke all refresh tokens for a user."""
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id, RefreshToken.is_revoked.is_(False)
            )
        )
        tokens = result.scalars().all()
        for token in tokens:
            token.is_revoked = True
            token.revoked_at = utcnow()
        await db.flush()

    @staticmethod
    async def rotate_refresh_token(
        db: AsyncSession, old_token: RefreshToken, user: User
    ) -> str:
        """Rotate refresh token - revoke old and create new."""
        # Revoke old token
        await AuthService.revoke_refresh_token(db, old_token)

        # Create new refresh token
        new_token_str = create_refresh_token({"sub": str(user.id)})
        await AuthService.create_refresh_token_record(db, user.id, new_token_str)

        return new_token_str

    @staticmethod
    async def cleanup_expired_tokens(db: AsyncSession) -> None:
        """Clean up expired refresh tokens (can be run periodically)."""
        await db.execute(delete(RefreshToken).where(RefreshToken.expires_at < utcnow()))
        await db.flush()
