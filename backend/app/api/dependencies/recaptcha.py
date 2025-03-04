import json
import httpx

from typing import Annotated, Optional
from fastapi import Body, HTTPException, Header, Depends, Request, status
from app.core.config import settings

async def validate_google_recaptcha(
    captcha: Optional[str] = Body(None),
) -> None:
    """Analyze the risk of a UI action.
    Args:
        project_id: Your Google Cloud Project ID.
        recaptcha_key: The reCAPTCHA key associated with the site/app
        token: The generated token obtained from the client.
        recaptcha_action: Action name corresponding to the token.
    """
    if settings.ENVIRONMENT == 'local' and settings.GOOGLE_RECAPTCA_SITEKEY is None:
        return
    if captcha is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing captcha token",
        )
    
    url = f"https://recaptchaenterprise.googleapis.com/v1/projects/{settings.GOOGLE_PROJECT_ID}/assessments?key={settings.GOOGLE_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "event": {
                "token": captcha,
                "siteKey": settings.GOOGLE_RECAPTCA_SITEKEY,
            },
        })
        response.raise_for_status()
        result = response.json()

    # Check if the token is valid.
    if not result["tokenProperties"]["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid captcha",
        )
  
ValidateGoogleRecaptchaDep = Annotated[str, Depends(validate_google_recaptcha)]
