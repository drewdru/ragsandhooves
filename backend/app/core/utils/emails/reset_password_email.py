from app.core.utils.email import EmailData, render_email_template
from app.core.config import settings
from app.core.utils.i18n import Translator

def generate_reset_password_email(email_to: str, email: str, token: str, lang: str = 'en') -> EmailData:
    i18n = Translator(lang)
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - {i18n.t('email.password_recovery_subject')}"
    link = f"{settings.FRONTEND_HOST}/auth/reset_password/{token}"
    html_content, txt_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
        lang=lang,
    )
    return EmailData(html_content=html_content, txt_content=txt_content, subject=subject)
