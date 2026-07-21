"""Email service — queues emails via Celery for async delivery."""

import logging
from app.workers.emails import send_email_task
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_verification_email(to: str, token: str) -> None:
    link = f"{settings.APP_URL}/verify?token={token}"
    send_email_task.delay(
        to=to,
        subject="Verify your email",
        body=f"Click here to verify: {link}",
    )
    logger.info("Verification email queued for %s", to)


def send_password_reset_email(to: str, token: str) -> None:
    link = f"{settings.APP_URL}/reset-password?token={token}"
    send_email_task.delay(
        to=to,
        subject="Reset your password",
        body=f"Click here to reset: {link}",
    )
    logger.info("Password reset email queued for %s", to)
