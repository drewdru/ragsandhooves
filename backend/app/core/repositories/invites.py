from sqlmodel import Session, select, func, select

from app.core.models.invite_users import InviteUsersLink
from app.core.models.invites import Invite

class InviteRepository:
    """Encapsulates all user-related database operations."""

    @staticmethod
    def get_invite_with_users_count(session: Session, invite: str):
        return session.exec(
            select(Invite, func.count(InviteUsersLink.user_id).label("user_count"))
            .join(InviteUsersLink, Invite.code == InviteUsersLink.invite_code)
            .where(Invite.code == invite)
            .group_by(Invite.id)
        ).one_or_none()