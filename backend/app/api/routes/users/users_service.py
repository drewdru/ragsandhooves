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
    def register_user(session: Session, user_in: UserRegister, invite: Invite | None) -> Any:
        """
        Create new user without the need to be logged in.
        """
        user = UserRepository.get_user_by_email(session=session, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system",
            )
        user_create = UserCreate.model_validate(user_in)
        user = UserRepository.create_user(session=session, user_create=user_create)
        # TODO: invite is None - create company and KB
        # TODO: else - connect to the company + add acess to KB if invite.knowledge_base_id else add acess to all KB
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
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return user

