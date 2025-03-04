from typing import Annotated
from fastapi import Header, HTTPException, Depends, Request, status

from app.api.dependencies.redis import RedisDep
from app.core.config import settings

def validate_csrf_token(request: Request, redis_client: RedisDep, csrf_token: str | None = Header(None, convert_underscores=False)) -> None:
    if not csrf_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token is missing")
    token_key = f"csrf_{csrf_token}"
    if not redis_client.exists(token_key):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")
    redis_client.delete(token_key)

ValidateCsrfTokenDep = Annotated[None, Depends(validate_csrf_token)]
