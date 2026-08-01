from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_admin_user
from app.models import AuthMessage
from app.utils import generate_test_email, send_email

router = APIRouter(prefix="/utils", tags=["utils"])


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_admin_user)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> AuthMessage:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return AuthMessage(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True