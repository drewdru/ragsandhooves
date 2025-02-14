from typing import Any

from app.core.repositories.users import UserRepository
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.core.security import get_password_hash
from app.core.dtos.message import Message
from app.core.dtos.password import NewPassword

from app.core.utils.email import (
    generate_reset_password_email,
    send_email,
)
from app.core.utils.password import (
    verify_password_reset_token,
    generate_password_reset_token,
)
from sqlmodel import Session

router = APIRouter(tags=["login"])


class PasswordRecoveryService:
    """Handles password-related business logic and database operations"""

    @staticmethod
    def recover_password(email: str, session: Session) -> Message:
        """
        Password Recovery
        """
        user = UserRepository.get_user_by_email(session=session, email=email)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this email does not exist in the system.",
            )
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
        return Message(message="Password recovery email sent")

    @staticmethod
    def reset_password(session: Session, body: NewPassword) -> Message:
        """
        Reset password
        """
        email = verify_password_reset_token(token=body.token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = UserRepository.get_user_by_email(session=session, email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this email does not exist in the system.",
            )
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        hashed_password = get_password_hash(password=body.new_password)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()
        return Message(message="Password updated successfully")

    @staticmethod
    def recover_password_html_content(email: str, session: Session) -> Any:
        """
        HTML Content for Password Recovery
        """
        user = UserRepository.get_user_by_email(session=session, email=email)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system.",
            )
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )

        return HTMLResponse(
            content=email_data.html_content, headers={"subject:": email_data.subject}
        )
