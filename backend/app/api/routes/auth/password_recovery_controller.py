from typing import Any, Optional

from app.api.dependencies.csrf_token import ValidateCsrfTokenDep
from app.api.dependencies.invite import InviteDep
from app.api.dependencies.lang_header import LangDep
from app.api.dependencies.recaptcha import ValidateGoogleRecaptchaDep
from app.core.dtos.users import UserAuth
from fastapi import APIRouter, Body, Depends, Response
from fastapi.responses import HTMLResponse

from app.api.dependencies.session import SessionDep
from app.api.dependencies.current_user import get_current_active_superuser

from app.core.dtos.message import Message
from app.core.dtos.password import NewPassword

from app.api.routes.auth.password_recovery_service import PasswordRecoveryService
from pydantic import EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/password-recovery")
def recover_password(
    _is_valid_csrf: ValidateCsrfTokenDep,
    _is_valid_recaptcha: ValidateGoogleRecaptchaDep,
    session: SessionDep,
    invite: InviteDep,
    lang: LangDep,
    email: EmailStr = Body(max_length=255),
) -> Message:
    """
    Password Recovery
    """
    return PasswordRecoveryService.recover_password(
        session, invite, email, lang
    )


@router.post("/reset-password", response_model=UserAuth)
def reset_password(
    _is_valid_csrf: ValidateCsrfTokenDep,
    response: Response,
    session: SessionDep,
    body: NewPassword
) -> UserAuth:
    """
    Reset password
    """
    return PasswordRecoveryService.reset_password(
        response, session, body
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
