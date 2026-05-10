from celery import shared_task
from service_objects.services import ServiceOutcome
from django.contrib.auth import get_user_model

from api.services import SendCurationEMail


@shared_task
def send_curations_to_users():
    users = get_user_model().objects.filter(
        email__isnull=False
    ).order_by("last_login")
    
    for u in users:
        send_single_curation_mail.delay(u)

@shared_task(bind=True, max_retries=3)
def send_single_curation_mail(self, user):
    try:
        ServiceOutcome(
            SendCurationEMail,
            {"user": user}
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)