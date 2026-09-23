import smtplib
import logging
from email.message import EmailMessage

from app.config import settings

logger = logging.getLogger("portfolio.email")


def send_contact_notification(name: str, email: str, message: str) -> None:
    """Best-effort email notification. Never raises: a failed email must not
    stop the contact message from being saved and returned as successful."""
    if not (settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASS):
        logger.info("SMTP not configured, skipping email notification")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = f"Portfolio message from {name}"
        msg["From"] = settings.SMTP_USER
        msg["To"] = settings.NOTIFY_EMAIL
        msg["Reply-To"] = email
        msg.set_content(f"From: {name} <{email}>\n\n{message}")

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
    except Exception:
        logger.exception("Failed to send contact notification email")