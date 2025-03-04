from typing import Any

from app.api.routes.auth.auth_service import AuthService
from app.core.dtos.users import UserAuth
from app.core.models.invites import Invite
from app.core.repositories.invites import InviteRepository
from app.core.repositories.users import UserRepository
from app.core.utils.emails.reset_password_email import generate_reset_password_email
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import HTMLResponse

from app.core.security import get_password_hash
from app.core.dtos.message import Message
from app.core.dtos.password import NewPassword
from app.core.config import settings

from app.core.utils.email import send_email
from app.core.utils.password import (
    verify_password_reset_token,
    generate_password_reset_token,
)
from sqlmodel import Session

router = APIRouter(tags=["login"])


class PasswordRecoveryService:
    """Handles password-related business logic and database operations"""

    @staticmethod
    def recover_password(
        session: Session,
        invite: Invite | None,
        email: str,
        lang: str,
    ) -> Message:
        """
        Password Recovery
        """
        user = UserRepository.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this email does not exist in the system.",
            )
        elif not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        password_reset_token = generate_password_reset_token(email=email)
        if invite is not None:
            InviteRepository.connect_invite_to_user(session, invite, user.id)
        if settings.emails_enabled:
            email_data = generate_reset_password_email(
                email_to=user.email, email=email, token=password_reset_token, lang=lang
            )
            send_email(
                email_to=user.email,
                email_data=email_data,
            )
        return Message(message="Password recovery email sent")

    @staticmethod
    def reset_password(
        response: Response,
        session: Session,
        body: NewPassword
    ) -> UserAuth:
        """
        Reset password
        """
        email = verify_password_reset_token(token=body.token)
        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        user = UserRepository.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this email does not exist in the system.",
            )
        elif not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        hashed_password = get_password_hash(password=body.new_password)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())

    @staticmethod
    def recover_password_html_content(email: str, session: Session) -> Any:
        """
        HTML Content for Password Recovery
        """
        user = UserRepository.get_user_by_email(session=session, email=email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this username does not exist in the system.",
            )
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )

        return HTMLResponse(
            content=email_data.html_content, headers={"subject:": email_data.subject}
        )
