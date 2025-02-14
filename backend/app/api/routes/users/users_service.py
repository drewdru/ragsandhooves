import uuid
from typing import Any
from app.core.repositories.users import UserRepository
from fastapi import APIRouter, HTTPException

from app.core.dtos.users import UserCreate, UserRegister
from app.core.models.users import User
from sqlmodel import Session

router = APIRouter(prefix="/users", tags=["users"])


class UsersService:
    """Handles users-related business logic and database operations"""

    @staticmethod
    def register_user(session: Session, user_in: UserRegister) -> Any:
        """
        Create new user without the need to be logged in.
        """
        user = UserRepository.get_user_by_email(session=session, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        user_create = UserCreate.model_validate(user_in)
        user = UserRepository.create_user(session=session, user_create=user_create)
        return user


    @staticmethod
    def read_user_by_id(
        user_id: uuid.UUID, session: Session, current_user: User
    ) -> Any:
        """
        Get a specific user by id.
        """
        user = session.get(User, user_id)
        if not current_user.is_superuser and user.id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="The user doesn't have enough privileges",
            )
        return user

