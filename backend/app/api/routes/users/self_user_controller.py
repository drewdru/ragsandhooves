from typing import Any
from app.api.routes.users.self_user_service import SelfUsersService
from fastapi import APIRouter

from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.core.dtos.message import Message
from app.core.dtos.users import UpdatePassword, UserPublic, UserUpdateMe

# route prefix couldn't be /users/me because users_controller has /{user_id} in path
router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """
    return SelfUsersService.update_user_me(session, user_in, current_user)


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    return SelfUsersService.update_password_me(session, body, current_user)


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    return SelfUsersService.delete_user_me(session, current_user)
