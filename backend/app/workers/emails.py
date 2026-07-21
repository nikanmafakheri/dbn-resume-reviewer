"""Async email delivery tasks."""

import logging
from app.workers.celery import celery_app
from app.clients.smtp import SMTPClient

logger = logging.getLogger(__name__)


@celery_app.task
def send_email_task(to: str, subject: str, body: str):
    """Send email via SMTP in the background."""
    client = SMTPClient()
    try:
        client.send(to, subject, body)
        logger.info("Email sent to %s", to)
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        raise
