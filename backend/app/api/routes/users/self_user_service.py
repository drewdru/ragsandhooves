from typing import Any
from app.core.models.users import User
from app.core.repositories.users import UserRepository
from app.core.services.users.validator import UsersValidationService
from fastapi import APIRouter, HTTPException

from app.core.security import verify_password
from app.core.dtos.message import Message
from app.core.dtos.users import UpdatePassword, UserUpdateMe
from sqlmodel import Session

# route prefix couldn't be /users/me because users_controller has /{user_id} in path
router = APIRouter(prefix="/users", tags=["users"])


class SelfUsersService:
    """Handles self users-related business logic and database operations"""

    @staticmethod
    def update_user_me(
        session: Session, user_in: UserUpdateMe, current_user: User
    ) -> Any:
        """
        Update own user.
        """
        if user_in.email:
            UsersValidationService.check_is_email_unique(
                session,
                user_in.email, 
                current_user.id,
            )
        return UserRepository.update_user(session=session, db_user=current_user, user_in=user_in)

    @staticmethod
    def update_password_me(
        session: Session, body: UpdatePassword, current_user: User
    ) -> Any:
        """
        Update own password.
        """
        if not verify_password(body.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        if body.current_password == body.new_password:
            raise HTTPException(
                status_code=400, detail="New password cannot be the same as the current one"
            )
        UserRepository.update_user(session=session, db_user=current_user, user_in={"password": body.new_password})
        return Message(message="Password updated successfully")

    @staticmethod
    def read_user_me(current_user: User) -> Any:
        """
        Get current user.
        """
        return current_user

    @staticmethod
    def delete_user_me(session: Session, current_user: User) -> Any:
        """
        Delete own user.
        """
        if current_user.is_superuser:
            raise HTTPException(
                status_code=403, detail="Super users are not allowed to delete themselves"
            )
        UserRepository.update_user(session=session, user=current_user)
        return Message(message="User deleted successfully")
