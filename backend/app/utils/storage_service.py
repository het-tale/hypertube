# services/storage_service.py
from fastapi import UploadFile
import aiofiles
from pathlib import Path
import uuid
from typing import Optional
from app.core.config import settings
import os

class StorageService:
    """Service for handling file storage operations."""
    
    def __init__(self, upload_dir: str = "uploads/profile_pictures"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_profile_picture(self, file: UploadFile, user_id: int) -> str:
        """
        Save profile picture and return URL/path.
        
        Args:
            file: The uploaded file
            user_id: ID of the user
            
        Returns:
            Relative path/URL to the saved file
        """
        # Generate unique filename
        filename = file.filename or "uploaded_file"
        file_extension = Path(filename).suffix
        unique_filename = f"{user_id}_{uuid.uuid4()}{file_extension}"
        file_path = self.upload_dir / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Return relative path (or full URL for production)
        return f"{settings.API_DOMAIN}/uploads/profile_pictures/{unique_filename}"
    
    async def delete_profile_picture(self, picture_url: str) -> None:
        """
        Delete profile picture file.
        
        Args:
            picture_url: URL/path to the picture to delete
        """
        try:
            # Extract filename from URL
            file_path = Path(picture_url.lstrip('/'))
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            # Log error but don't fail the operation
            print(f"Error deleting profile picture: {e}")


# Initialize storage service
storage_service = StorageService()