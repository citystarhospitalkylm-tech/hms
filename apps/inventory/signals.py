from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.pharmacy.models import SaleItem
from .models import StockChange

@receiver(post_save, sender=SaleItem)
def log_sale_stock_change(sender, instance, created, **kwargs):
    if not created:
        return

    # record negative delta on sale
    StockChange.objects.create(
        user      = instance.sale.sold_by,
        medicine  = instance.medicine,
        batch     = instance.batch,
        delta     = -instance.quantity,
        sale_item = instance,
        note      = f"Sold via sale {instance.sale.id}"
    )