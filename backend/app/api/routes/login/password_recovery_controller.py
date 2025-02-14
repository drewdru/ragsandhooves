from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.api.deps import SessionDep, get_current_active_superuser

from app.core.dtos.message import Message
from app.core.dtos.password import NewPassword

from app.api.routes.login.password_recovery_service import PasswordRecoveryService

router = APIRouter(tags=["login"])


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    return PasswordRecoveryService.recover_password(
        email, session
    )


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    return PasswordRecoveryService.reset_password(
        session, body
    )


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    return PasswordRecoveryService.recover_password_html_content(
        email, session
    )
