import uuid
from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from app.core.config import settings
from app.core.dtos.message import Message
from app.core.dtos.users import UserCreate, UserUpdate
from app.core.models.users import User
from app.core.utils.email import generate_new_account_email, send_email
from app.core.repositories.users import UserRepository
from app.core.services.users.validator import UsersValidationService

router = APIRouter(prefix="/users", tags=["users"])




class AdminUsersService:
    """Handles admin users-related business logic and database operations"""

    @staticmethod
    def create_user(session: Session, user_in: UserCreate) -> Any:
        """
        Create new user.
        """
        user = UserRepository.get_user_by_email(session=session, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        user = UserRepository.create_user(session=session, user_create=user_in)
        if settings.emails_enabled and user_in.email:
            email_data = generate_new_account_email(
                email_to=user_in.email, username=user_in.email, password=user_in.password
            )
            send_email(
                email_to=user_in.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        return user


    @staticmethod
    def update_user(
        session: Session,
        current_user: User,
        user_id: uuid.UUID,
        user_in: UserUpdate,
    ) -> Any:
        """
        Update a user.
        """
        db_user = UserRepository.get_user_by_id(session, current_user, user_id)
        UsersValidationService.check_current_user_permissions(db_user, current_user)
        if user_in.email:
            UsersValidationService.check_is_email_unique(
                session,
                user_in.email, 
                user_id,
            )
        return UserRepository.update_user(session=session, db_user=db_user, user_in=user_in)

    @staticmethod
    def delete_user(
        session: Session, current_user: User, user_id: uuid.UUID
    ) -> Message:
        """
        Delete a user.
        """
        user = UserRepository.get_user_by_id(session, current_user, user_id)
        UsersValidationService.check_current_user_permissions(user, current_user)
        if user == current_user and current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="Super users are not allowed to delete themselves"
            )
        UserRepository.delete_user_by_id(session, user)
        return Message(message="User deleted successfully")
