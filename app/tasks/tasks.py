import smtplib

from app.config import settings
from app.tasks.celery_app import celery
from app.tasks.email_templates import create_confirmation


@celery.task
def send_message(email_to:str):
    content = create_confirmation(email_to)

    with smtplib.SMTP_SSL(settings.GM_HOST, settings.GM_PORT) as server:
        server.login(settings.GM_USER, settings.GM_PASSWORD)
        server.send_message(content)

