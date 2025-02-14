from datetime import timedelta
from typing import Annotated

from app.core.repositories.users import UserRepository
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.core.dtos.token import Token
from sqlmodel import Session

router = APIRouter(tags=["login"])


class LoginService:
    """Handles login-related business logic and database operations"""

    @staticmethod
    def login_access_token(
        session: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
        """
        OAuth2 compatible token login, get an access token for future requests
        """
        user = UserRepository.authenticate(
            session=session, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            )
        )
