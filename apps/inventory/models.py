from django.db import models

class InventoryRecord(models.Model):
    """
    Tracks current stock position per drug batch,
    without importing pharmacy models directly.
    """

    batch = models.OneToOneField(
        "pharmacy.Batch",
        on_delete=models.PROTECT,
        related_name="inventory_record"
    )
    # Optionally link to the last sale item
    last_sale = models.ForeignKey(
        "pharmacy.SaleItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )
    current_quantity = models.PositiveIntegerField(default=0)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["batch__drug__name"]
        verbose_name = "Inventory Record"
        verbose_name_plural = "Inventory Records"

    def __str__(self):
        drug = self.batch.drug
        return f"{drug.name} — Batch {self.batch.batch_no}: {self.current_quantity} units"