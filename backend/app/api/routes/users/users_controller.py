import uuid
from typing import Any
from app.api.routes.users.users_service import UsersService
from fastapi import APIRouter

from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.core.dtos.users import UserPublic, UserRegister

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    return UsersService.register_user(session, user_in)


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    return UsersService.read_user_by_id(user_id, session, current_user)
