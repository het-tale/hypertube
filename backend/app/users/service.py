"""User service layer for business logic."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.models import User
from app.users.schemas import UserCreate


class UserService:
    """Service layer for user operations."""

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            profile_picture=user_in.profile_picture
        )
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        """ Get User by username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()


    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> User | None:
        """Authenticate user with email and password."""
        user = await UserService.get_by_email(db, email)
        if not user:
            return None
        if not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
