from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login_form"
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]
