from celery import shared_task
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from .models import Admission

@shared_task
def daily_occupancy_report():
    total = Admission.objects.filter(status='admitted').count()
    ward_counts = Admission.objects.filter(status='admitted') \
        .values('ward__name') \
        .annotate(count=Count('id'))
    body = [f"Total admitted: {total}"]
    for w in ward_counts:
        body.append(f"{w['ward__name']}: {w['count']}")
    send_mail(
        "Daily IPD Occupancy Report",
        "\n".join(body),
        settings.DEFAULT_FROM_EMAIL,
        [settings.IPD_MANAGER_EMAIL],
    )