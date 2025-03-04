from datetime import datetime, timedelta, timezone
import secrets
from typing import Annotated, Any, Optional
import uuid

from app.core.dtos.message import Message
from app.core.dtos.users import UserAuth, UserCreate, UserRegister, UserUpdate, UserUpdateVerifyToken
from app.core.models.invites import Invite
from app.core.models.users import User
from app.core.repositories.invites import InviteRepository
from app.core.repositories.users import UserRepository
from app.core.utils.email import send_email
from app.core.utils.emails.new_account_email import generate_new_account_email
from app.core.utils.env_helpers import parse_expire
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.core.dtos.token import CsrfToken, Token, TokenPayload
import jwt
from pydantic import ValidationError
from redis import Redis
from sqlmodel import Session


class AuthService:
    """Handles login-related business logic and database operations"""

    @staticmethod
    def generate_auth_tokens(
        response: Response,
        user_id: str
    ) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = security.create_token(
            user_id, expires_delta=refresh_token_expires
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return Token(
            access_token=security.create_token(
                user_id, expires_delta=access_token_expires
            ),
            refresh_token=refresh_token,
        )
        
    @staticmethod
    def login_access_token(
        session: Session,
        response: Response,
        form_data: OAuth2PasswordRequestForm,
        invite: Invite | None,
    ) -> UserAuth:
        """
        OAuth2 compatible token login, get an access token for future requests
        """
        user = UserRepository.authenticate(
            session=session, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
        elif not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        if invite is not None:
            InviteRepository.connect_invite_to_user(session, invite, user.id)
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())

    
    @staticmethod
    def refresh_token(
        response: Response,
        session: Session,
        refresh_token: Optional[str],
    ) -> UserAuth:
        if not refresh_token:
            response.delete_cookie("refresh_token")
            raise HTTPException(status_code=403, detail="Refresh token missing")
        
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except (jwt.InvalidTokenError, ValidationError):
            response.delete_cookie("refresh_token")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user = session.get(User, token_data.sub)
        if not user:
            response.delete_cookie("refresh_token")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.is_active:
            response.delete_cookie("refresh_token")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())

    @staticmethod
    def register_user(
        redis_client: Redis,
        session: Session,
        user_in: UserRegister,
        invite: Invite | None,
        lang: str,
        response: Response,
    ) -> UserAuth:
        """
        Create new user without the need to be logged in.
        """
        user = UserRepository.get_user_by_email(session=session, email=user_in.email)
        if user and user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system",
            )
        if not user:
            user_create = UserCreate.model_validate(user_in)
            user = UserRepository.create_user(session=session, user_create=user_create)
        if invite is not None:
            InviteRepository.connect_invite_to_user(session, invite, user.id)
        if settings.emails_enabled:
            email_data = generate_new_account_email(
                email_to=user_in.email,
                token=user.verify_token,
                lang=lang,
            )
            is_success = send_email(
                email_to=user_in.email,
                email_data=email_data,
            )
            if is_success:
                expire_delta = timedelta(minutes=settings.VERIFY_TOKEN_RESEND_EXPIRE_MINUTES)
                redis_client.set(f"verify_token_{user.verify_token}", "1", px=expire_delta, nx=True)
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())

    @staticmethod
    def generate_csrf_token(redis_client: Redis, expire: Optional[str]) -> CsrfToken:
        """
        Generate new csrf token
        """
        csrf_token = secrets.token_hex(32)
        if expire is None:
            expire_delta = timedelta(minutes=settings.CSRF_TOKEN_EXPIRE_MINUTES)
        else:
            expire_delta = parse_expire(expire)
        redis_client.set(f"csrf_{csrf_token}", "1", px=expire_delta, nx=True)
        return CsrfToken(token=csrf_token, expire=(datetime.now(timezone.utc) + expire_delta))


    @staticmethod
    def verify_email(
        response: Response,
        session: Session,
        token: str,
    ) -> UserAuth:
        """
        Verify user email.
        """
        user = UserRepository.get_user_by_verify_token(session=session, token=token)
        if user and user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user's email already verified",
            )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verify token is invalid",
            )
        UserRepository.update_user(session, user, UserUpdate(is_verified=True))
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())

    @staticmethod
    def resend_verify_token(
        redis_client: Redis, 
        session: Session,
        user: User,
        lang: str,
    ) -> Message:
        """
        Create new user without the need to be logged in.
        """
        if user and user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user's email already verified",
            )
        if redis_client.exists(f"verify_token_{user.verify_token}"):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Already sent")
        user.sqlmodel_update(UserUpdateVerifyToken(verify_token=uuid.uuid4()))
        session.add(user)
        session.commit()
        session.refresh(user)
        if settings.emails_enabled:
            email_data = generate_new_account_email(
                email_to=user.email,
                token=user.verify_token,
                lang=lang,
            )
            is_success = send_email(
                email_to=user.email,
                email_data=email_data,
            )
            if is_success:
                expire_delta = timedelta(minutes=settings.VERIFY_TOKEN_RESEND_EXPIRE_MINUTES)
                redis_client.set(f"verify_token_{user.verify_token}", "1", px=expire_delta, nx=True)
        return Message(message="Verify email sent")