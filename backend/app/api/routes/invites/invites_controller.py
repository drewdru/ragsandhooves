from app.api.dependencies.invite import InviteDep
from fastapi import APIRouter

from app.api.dependencies.session import SessionDep
from app.api.dependencies.current_user import CurrentUserDep

from app.core.dtos.users import UserAuth

from .invites_service import InviteService

router = APIRouter(prefix="/invites", tags=["auth"])

@router.post("/", response_model=UserAuth)
def connect_invite(
    session: SessionDep,
    invite: InviteDep,
    user: CurrentUserDep,
) -> UserAuth:
    """
    Connect company invite and KBs to user
    """
    return InviteService.connect_user(session, invite, user)
