

import httpx
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from sqlmodel import Session

from fastapi import HTTPException, Request, Response, requests, status
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.api.routes.auth.auth_service import AuthService
from app.core.dtos.users import UserAuth, UserCreate, UserUpdate
from app.core.models.invites import Invite
from app.core.repositories.invites import InviteRepository
from app.core.repositories.users import UserRepository
from app.tests.utils.utils import random_lower_string

class LoginGoogleService:
    @staticmethod
    async def login(request: Request, invite: Invite | None):
        state = invite if invite is not None else ""        
        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_AUTH_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope=openid email profile"
            f"&state={state}"
        )
        return RedirectResponse(url=google_auth_url)

    @staticmethod
    async def google_login_callback(
        response: Response,
        request: Request,
        session: Session,
        invite: Invite | None,
        code: str,
        scope: str,
    ):
        token_request_uri = "https://oauth2.googleapis.com/token"
        data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_AUTH_REDIRECT_URI,
            'grant_type': 'authorization_code',
            'code': code,
        }
        async with httpx.AsyncClient() as client:
            auth_response = await client.post(token_request_uri, data=data)
            auth_response.raise_for_status()
            token_data = auth_response.json()

        id_token_value = token_data.get("id_token")
        if not id_token_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )
            
        id_info = id_token.verify_oauth2_token(id_token_value, GoogleRequest(), settings.GOOGLE_CLIENT_ID)
        if not id_info.get("email_verified"):
            raise HTTPException(status_code=400, detail="Email is not verified")
        google_id = id_info.get("sub")
        email = id_info.get("email")
        full_name = id_info.get("name")
        avatar = id_info.get("picture")
        user = UserRepository.get_user_by_email(session=session, email=email)
        if user and not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        elif user:
            UserRepository.update_user(session, user, UserUpdate(
                is_verified=True,
                full_name=full_name,
                avatar=avatar,
                google_id=google_id,
            ))
        else:
            user_create = UserCreate(
                email=email,
                full_name=full_name,
                avatar=avatar,
                is_verified=True,
                google_id=google_id,
                password=random_lower_string(),
            )
            user = UserRepository.create_user(session=session, user_create=user_create)
        if invite is not None:
            InviteRepository.connect_invite_to_user(session, invite, user.id)
        tokens = AuthService.generate_auth_tokens(response, user.id)
        return UserAuth(**user.model_dump(), **tokens.model_dump())




