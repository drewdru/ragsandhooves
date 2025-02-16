from datetime import datetime
from typing import Annotated, Tuple

from app.core.models.invites import Invite
from app.core.repositories.invites import InviteRepository
from fastapi import HTTPException, Query, Depends, status

from app.api.dependencies.session import SessionDep

def get_invite(
    session: SessionDep,
    invite: str | None = Query(None, description="Invite code"),
) -> Invite | None:
    if not invite:
        return None
    
    result = InviteRepository.get_invite_with_users_count(session, invite)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
    
    invite_data, user_count = result
    if not invite_data.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite expired")
    if invite_data.expires_at and invite_data.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite expired")
    if invite_data.max_users and invite_data.max_users <= user_count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Max users reached for this invite")
    return invite_data

InviteDep = Annotated[Invite | None, Depends(get_invite)]
