from app.core.utils.email import EmailData, render_email_template
from app.core.config import settings
from app.core.utils.i18n import Translator


def generate_test_email(email_to: str, lang: str = 'en') -> EmailData:
    i18n = Translator(lang)
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - {i18n.t('email.test_email_subject')}"
    html_content, txt_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
        lang=lang
    )
    return EmailData(html_content=html_content, txt_content=txt_content, subject=subject)
