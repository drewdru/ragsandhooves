from typing import Any

from app.core.repositories.users import UserRepository
from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.dtos.users import PrivateUserCreate, UserPublic

router = APIRouter(tags=["users"], prefix="/private/users")


@router.post("/", response_model=UserPublic)
def create_user(user_in: PrivateUserCreate, session: SessionDep) -> Any:
    """
    Create a new user.
    """
    return UserRepository.create_private_user(session, user_in)
