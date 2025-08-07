from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from .models import Stock

LOW_STOCK_THRESHOLD = 10

@receiver(post_save, sender=Stock)
def notify_low_stock(sender, instance, **kwargs):
    total_qty = instance.drug.stocks.aggregate(
        total=models.Sum('quantity')
    )['total'] or 0

    if total_qty < LOW_STOCK_THRESHOLD:
        subject = f"Low Stock Alert: {instance.drug.name}"
        message = (
            f"Current total stock ({total_qty}) of {instance.drug.name} "
            f"is below threshold ({LOW_STOCK_THRESHOLD}). Please reorder."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.PHARMACY_MANAGER_EMAIL],
        )