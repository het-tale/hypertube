"""User service layer for business logic."""
from typing import Optional
import uuid
from fastapi import Path, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.models import User
from app.users.expection import EmailAlreadyInUse, UserNotFoundException, UsernameAlreadyInUse
from app.users.schemas import UserCreate, UserUpdate
import aiofiles
from app.utils.storage_service import storage_service



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
    
    @staticmethod
    async def update_user_info_deprecated(db: AsyncSession, id : int, updated_data : UserUpdate):
        
        user = await UserService.get_by_id(db, id)
        if not user:
            raise UserNotFoundException("User not found")
        data = updated_data.model_dump(exclude_unset=True, exclude_none=True)
        if not data:
            return None
        if "email" in data and data["email"] != user.email:
            user1 = await UserService.get_by_email(db, data['email'])
            if user1:
                raise EmailAlreadyInUse("New Email is alreadu used")
        if "username" in data and data['username'] != user.username:
            user1 = await UserService.get_by_username(db,data['username'])
            if user1:
                raise UsernameAlreadyInUse
            
        for field, value in data.items():
            setattr(user, field, value)
        # 6) Persist changes in the current transaction
        await db.flush()
        await db.refresh(user)

        return user
    # services/user_service.py
    @staticmethod
    async def _save_profile_picture(file: UploadFile, user_id: int) -> str:
        """Save profile picture and return relative URL."""
    
        upload_dir = Path("uploads/profile_pictures")
        upload_dir.mkdir(parents=True, exist_ok=True)
    
        file_extension = Path(file.filename).suffix
        unique_filename = f"{user_id}_{uuid.uuid4()}{file_extension}"
        file_path = upload_dir / unique_filename
    
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    
        # Return relative path - FastAPI will serve it from /uploads
        return f"/uploads/profile_pictures/{unique_filename}"


    @staticmethod
    async def update_user_info(
        db: AsyncSession,
        user_id: int,
        updated_data: UserUpdate,
        profile_picture: Optional[UploadFile] = None
    ) -> User:
        """
        Update user information and optionally profile picture.
        
        Args:
            db: Database session
            user_id: ID of the user to update
            updated_data: Data to update
            profile_picture: Optional profile picture file
            
        Returns:
            Updated user object
            
        Raises:
            UserNotFoundException: If user is not found
            EmailAlreadyInUse: If email is already taken
            UsernameAlreadyInUse: If username is already taken
        """
        # 1) Get user
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise UserNotFoundException("User not found")
        
        # 2) Extract data to update (excluding None and unset fields)
        data = updated_data.model_dump(exclude_unset=True, exclude_none=True)
        print("Data extracted for update:", data)  # Debugging statement
        
        # 3) Validate email uniqueness if changing
        if "email" in data and data["email"] != user.email:
            existing_user = await UserService.get_by_email(db, data["email"])
            if existing_user:
                raise EmailAlreadyInUse("Email is already in use")
        
        # 4) Validate username uniqueness if changing
        if "username" in data and data["username"] != user.username:
            existing_user = await UserService.get_by_username(db, data["username"])
            if existing_user:
                raise UsernameAlreadyInUse("Username is already in use")
        
        # 5) Handle profile picture upload
        if profile_picture:
            # Save new picture
            picture_url = await storage_service.save_profile_picture(
                profile_picture, user_id
            )
            data["profile_picture"] = picture_url
            
            # Delete old profile picture if exists
            if user.profile_picture:
                await storage_service.delete_profile_picture(user.profile_picture)
        

        print("Data to update:", data)  # Debugging statement
        # 6) Apply updates to user object
        for field, value in data.items():
            setattr(user, field, value)

        
        
        # 7) Persist changes
        await db.flush()
        print("Updated user:", user.__dict__)  # Debugging statement
        # await db.refresh(user)
        print("Updated user 2:", user.__dict__)  # Debugging statement
        
        return user