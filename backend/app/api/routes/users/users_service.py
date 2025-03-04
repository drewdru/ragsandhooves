import uuid
from typing import Any
from app.core.models.invites import Invite
from app.core.repositories.users import UserRepository
from fastapi import APIRouter, HTTPException, status

from app.core.dtos.users import UserCreate, UserRegister
from app.core.models.users import User
from sqlmodel import Session

router = APIRouter(prefix="/users", tags=["users"])


class UsersService:
    """Handles users-related business logic and database operations"""

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
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return user

