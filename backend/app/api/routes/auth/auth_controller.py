from typing import Annotated, Any, Optional

from app.api.dependencies.csrf_token import ValidateCsrfTokenDep
from app.api.dependencies.invite import InviteDep
from app.api.dependencies.lang_header import LangDep
from app.api.dependencies.recaptcha import ValidateGoogleRecaptchaDep
from app.api.dependencies.redis import RedisDep
from app.api.dependencies.webhook_auth import ValidateSystemWebhookTokenDep
from app.core.dtos.message import Message
from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.session import SessionDep
from app.api.dependencies.current_user import CurrentUserDep

from app.core.dtos.auth_token import CsrfToken, Token
from app.core.dtos.users import UserAuth, UserPublic, UserRegister

from .auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login_form", response_model=UserAuth)
def login_access_token(
    session: SessionDep,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> UserAuth:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return AuthService.login_access_token(
        session, response, form_data
    )
    
@router.post("/login", response_model=UserAuth)
def login_access_token(
    _is_valid_csrf: ValidateCsrfTokenDep,
    _is_valid_recaptcha: ValidateGoogleRecaptchaDep,
    session: SessionDep,
    response: Response,
    invite: InviteDep,
    email: str = Body(...),
    password: str = Body(...),
) -> UserAuth:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    return AuthService.login_access_token(
        session,
        response,
        OAuth2PasswordRequestForm(
            username=email,
            password=password
        ),
        invite,
    )

@router.post("/logout")
def logout(
    response: Response,
) -> Any:
    """
    Logout
    """
    response.delete_cookie("refresh_token")


@router.post("/refresh-token", response_model=UserAuth)
def refresh_token(
    response: Response,
    session: SessionDep,
    refresh_token: Optional[str] = Cookie(None),
) -> UserAuth:
    """
    Refresh the access token using the refresh token stored in HTTP-only cookie.
    """
    return AuthService.refresh_token(
        response, session, refresh_token
    )

@router.post("/csrf-token")
def generate_csrf_token(
    _: ValidateSystemWebhookTokenDep,
    redis_client: RedisDep,
    expire: Optional[str] = Body(None, embed=True),
) -> CsrfToken:
    """
    Generate new csrf token
    """
    return AuthService.generate_csrf_token(
        redis_client, expire
    )

@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUserDep) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/signup", response_model=UserAuth)
def register_user(
    _: ValidateCsrfTokenDep,
    redis_client: RedisDep,
    session: SessionDep,
    user_in: UserRegister,
    invite: InviteDep,
    lang: LangDep,
    response: Response,
) -> UserAuth:
    """
    Create new user without the need to be logged in.
    """
    return AuthService.register_user(redis_client, session, user_in, invite, lang, response)


@router.post("/verify-email", response_model=UserAuth)
def verify_email(
    _is_valid_csrf: ValidateCsrfTokenDep,
    response: Response,
    session: SessionDep,
    token: str = Body(...),
) -> UserAuth:
    """
    Verify email
    """
    return AuthService.verify_email(
        response, session, token
    )


@router.post("/resend-verify-token")
def resend_verify_token(
    redis_client: RedisDep,
    session: SessionDep,
    lang: LangDep,
    current_user: CurrentUserDep,
) -> Message:
    """
    Verify email
    """
    return AuthService.resend_verify_token(
        redis_client, session, current_user, lang
    )

