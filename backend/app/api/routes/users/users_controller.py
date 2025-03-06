import uuid
from typing import Any
from app.api.routes.users.users_service import UsersService
from fastapi import APIRouter

from app.core.dtos.users import UserPublic

from app.api.dependencies.session import SessionDep
from app.api.dependencies.current_user import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
) -> Any:
    """
    Get a specific user by id.
    """
    return UsersService.read_user_by_id(user_id, session, current_user)
