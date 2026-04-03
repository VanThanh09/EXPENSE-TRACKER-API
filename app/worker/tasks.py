import logging

from app.worker.celery_app import celery
from app.utils import render_email_template

from email.mime.text import MIMEText
import smtplib
from app.core.config import settings

logger = logging.getLogger(__name__)


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def send_email_welcome(self, email: str) -> dict:
    html = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": "Blog-API",
            "link": "https://github.com/VanThanh09/BLOG-API/"
        }
    )

    msg = MIMEText(html, "html")
    msg["Subject"] = "Welcome to Blog-API"
    msg["From"] = settings.mail_from
    msg["To"] = email

    with smtplib.SMTP(settings.mail_server, settings.mail_port, timeout=10) as server:
        server.starttls()
        server.login(settings.mail_username, settings.mail_password)
        server.send_message(msg)

    logger.info(f"Sending email to {email}")

    return {"success": True, "to": email}
