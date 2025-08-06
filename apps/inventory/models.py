from django.db import models
from django.utils import timezone
from apps.pharmacy.models import Medicine, Batch, SaleItem
from django.contrib.auth import get_user_model

User = get_user_model()


class StockChange(models.Model):
    """
    Records every decrement or increment to batch stock.
    Negative `delta` means stock went down.
    """
    timestamp   = models.DateTimeField(default=timezone.now)
    user        = models.ForeignKey(User, on_delete=models.PROTECT)
    medicine    = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch       = models.ForeignKey(Batch, on_delete=models.PROTECT)
    delta       = models.IntegerField()  # +ve for receipts, -ve for issues
    sale_item   = models.ForeignKey(
        SaleItem,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="If change caused by a SaleItem"
    )
    note        = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        direction = "↓" if self.delta < 0 else "↑"
        return f"{direction} {self.medicine.name} ({self.batch.batch_number}): {self.delta}"