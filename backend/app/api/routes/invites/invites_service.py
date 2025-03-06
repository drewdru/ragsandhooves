from app.core.models.invites import Invite
from app.core.models.users import User
from app.core.repositories.invites import InviteRepository
from sqlmodel import Session


class InviteService:
    """Handles invites-related business logic and database operations"""

    @staticmethod
    def connect_user(
        session: Session,
        invite: Invite | None,
        user: User,
    ) -> None:
        """
        Connect company invite and KBs to user
        """
        if invite is not None:
            InviteRepository.connect_invite_to_user(session, invite, user.id)

