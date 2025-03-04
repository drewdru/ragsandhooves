import logging
from app.core.utils.i18n import Translator
import emails  # type: ignore

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Template

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmailData:
    html_content: str
    txt_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any], lang: str = 'en') -> tuple[str, str]:
    context["_"] = Translator(lang).t
    template_str = (
        Path(__file__).parent / ".." / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    txt_str = (
        Path(__file__).parent / ".." / "email-templates" / "build" / f"{template_name}.txt"
    ).read_text()
    txt_content = Template(txt_str).render(context)
    return html_content, txt_content


def send_email(
    *,
    email_to: str,
    email_data: EmailData,
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=email_data.subject,
        html=email_data.html_content,
        text=email_data.txt_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logger.info(f"send email result: {response}")
    return response.success
