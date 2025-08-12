from django.db import models
from django.db.models import Sum

class Supplier(models.Model):
    name          = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField()
    phone         = models.CharField(max_length=20, blank=True)
    address       = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.name

class DrugCategory(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Drug Category"
        verbose_name_plural = "Drug Categories"

    def __str__(self):
        return self.name

class Drug(models.Model):
    name        = models.CharField(max_length=255)
    category    = models.ForeignKey(
        DrugCategory,
        on_delete=models.PROTECT,
        related_name="drugs"
    )
    description = models.TextField(blank=True)
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["name", "category"]]
        ordering = ["category__name", "name"]
        verbose_name = "Drug"
        verbose_name_plural = "Drugs"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Batch(models.Model):
    drug        = models.ForeignKey(
        Drug,
        on_delete=models.PROTECT,
        related_name="batches"
    )
    supplier    = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="batches"
    )
    batch_no    = models.CharField(max_length=100)  # unique per drug via Meta.unique_together
    expiry_date = models.DateField()
    quantity    = models.PositiveIntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-expiry_date", "batch_no"]
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
        unique_together = ("drug", "batch_no")

    def __str__(self):
        return f"Batch {self.batch_no} – {self.drug.name}"

    @property
    def total_sold(self):
        return self.sale_items.aggregate(total=Sum("quantity_sold"))["total"] or 0

    @property
    def available_quantity(self):
        return self.quantity - self.total_sold

class SaleItem(models.Model):
    batch         = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name="sale_items"
    )
    quantity_sold = models.PositiveIntegerField()
    sold_at       = models.DateTimeField(auto_now_add=True)
    unit_price    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-sold_at"]
        verbose_name = "Sale Item"
        verbose_name_plural = "Sale Items"

    def __str__(self):
        return f"{self.quantity_sold}×{self.batch.drug.name} on {self.sold_at.date()}"