from app.core.utils.emails.test_email import generate_test_email
from fastapi import APIRouter, Depends, status
from pydantic.networks import EmailStr

from app.api.dependencies.current_user import get_current_active_superuser
from app.core.dtos.message import Message
from app.core.utils.email import send_email

router = APIRouter(prefix="/utils", tags=["utils"])


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=status.HTTP_201_CREATED,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        email_data=email_data,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True
