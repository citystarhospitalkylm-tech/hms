from celery import shared_task
from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from .models import Drug, Stock

@shared_task
def check_all_drugs_stock():
    """
    Daily scheduled task to scan all drugs and trigger low-stock emails.
    """
    threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 10)
    for drug in Drug.objects.all():
        total = drug.stocks.aggregate(total=models.Sum('quantity'))['total'] or 0
        if total < threshold:
            send_mail(
                f"Low Stock Alert: {drug.name}",
                f"{drug.name} stock is {total}, below threshold {threshold}.",
                settings.DEFAULT_FROM_EMAIL,
                [settings.PHARMACY_MANAGER_EMAIL],
            )