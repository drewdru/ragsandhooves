from typing import Annotated
from fastapi import HTTPException, Header, Depends, status
from app.core.config import settings

def validate_system_webhook_token(authorization: str | None = Header(None)) -> str:
    """
    Extracts the authorization from the header.
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    if authorization not in settings.all_system_webhook_tokens:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

ValidateSystemWebhookTokenDep = Annotated[str, Depends(validate_system_webhook_token)]