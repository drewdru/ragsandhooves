from app.api.dependencies.invite import InviteDep
from app.api.dependencies.lang_header import LangDep
from app.api.dependencies.session import SessionDep
from app.api.routes.auth.login_google_service import LoginGoogleService
from fastapi import APIRouter, Body, Query, Request, Response
from app.core.config import settings
from fastapi.responses import RedirectResponse
import httpx

router = APIRouter(prefix="/auth/google", tags=["auth"])


@router.get("/")
async def login(
    request: Request,
    invite: InviteDep,
):
    return await LoginGoogleService.login(request, invite)

@router.post("/login")
async def google_login_callback(
    response: Response,
    request: Request,
    invite: InviteDep,
    session: SessionDep,
    code: str | None = Body(..., description="Google auth code"),
    scope: str | None = Body(None, description="Google auth scope"),
):
    return await LoginGoogleService.google_login_callback(response, request, session, invite, code, scope)
