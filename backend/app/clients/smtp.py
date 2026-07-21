"""SMTP email client."""

import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


class SMTPClient:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD

    def send(self, to: str, subject: str, body: str) -> None:
        if not self.host:
            return  # silently skip if SMTP not configured (dev)

        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            if self.user:
                server.login(self.user, self.password)
            server.send_message(msg)
