import uuid
from django.db import models, transaction
from django.utils import timezone
from apps.patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class Medicine(models.Model):
    name                = models.CharField(max_length=200, unique=True)
    description         = models.TextField(blank=True)
    unit_price          = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        return sum(batch.quantity for batch in self.batches.all())


class Batch(models.Model):
    medicine     = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name='batches'
    )
    batch_number = models.CharField(max_length=50)
    expiry_date  = models.DateField()
    quantity     = models.PositiveIntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('medicine', 'batch_number')
        ordering = ['expiry_date']

    def __str__(self):
        return f"{self.medicine.name} | Batch {self.batch_number}"


class PharmacySale(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient       = models.ForeignKey(Patient, on_delete=models.PROTECT)
    sale_date     = models.DateTimeField(auto_now_add=True)
    sold_by       = models.ForeignKey(User, on_delete=models.PROTECT)
    prescription  = models.OneToOneField(
        'consultations.Prescription',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='pharmacy_sale'
    )

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale {self.id} for {self.patient.patient_id}"

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class SaleItem(models.Model):
    sale         = models.ForeignKey(
        PharmacySale, on_delete=models.CASCADE, related_name='items'
    )
    medicine     = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch        = models.ForeignKey(Batch, on_delete=models.PROTECT)
    quantity     = models.PositiveIntegerField()
    unit_price   = models.DecimalField(max_digits=10, decimal_places=2)
    total_price  = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        ordering = ['medicine__name']

    def save(self, *args, **kwargs):
        # calculate total_price
        self.unit_price = self.unit_price or self.medicine.unit_price
        self.total_price = self.unit_price * self.quantity

        # atomic stock decrement
        with transaction.atomic():
            batch = Batch.objects.select_for_update().get(pk=self.batch.pk)
            if batch.quantity < self.quantity:
                raise ValueError(f"Insufficient stock in batch {batch.batch_number}")
            batch.quantity -= self.quantity
            batch.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name}"