import uuid
from app.core.repositories.users import UserRepository
from fastapi import HTTPException, status
from sqlmodel import Session
from app.core.models.users import User


class UsersValidationService:
    @staticmethod
    def check_current_user_permissions(user: User, current_user: User):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not current_user.is_superuser and (user.id != current_user.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
        
    @staticmethod
    def check_is_email_unique(
        session: Session,
        email: str, 
        user_id: uuid.UUID,
    ):
        existing_user = UserRepository.get_user_by_email(session=session, email=email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists"
            )
