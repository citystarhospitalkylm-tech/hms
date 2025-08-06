import uuid
from django.db import models, transaction
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT            = 'DRAFT',            'Draft'
        PARTIALLY_PAID   = 'PARTIAL',          'Partially Paid'
        PAID             = 'PAID',             'Paid'
        OVERDUE          = 'OVERDUE',          'Overdue'

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequence        = models.PositiveIntegerField(editable=False, unique=True)
    invoice_number  = models.CharField(max_length=30, unique=True, editable=False)
    patient         = models.ForeignKey('patients.Patient', on_delete=models.PROTECT)
    created_by      = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at      = models.DateTimeField(auto_now_add=True)
    due_date        = models.DateField()
    status          = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                last_seq = Invoice.objects.aggregate(models.Max('sequence'))['sequence__max'] or 0
                self.sequence = last_seq + 1
                today = timezone.now().strftime('%Y%m%d')
                self.invoice_number = f"BIL-{today}-{self.sequence:06d}"
        super().save(*args, **kwargs)
        # Update status
        if self.outstanding_amount <= 0:
            self.status = Invoice.Status.PAID
        elif self.due_date < timezone.now().date():
            self.status = Invoice.Status.OVERDUE
        elif self.payments.exists():
            self.status = Invoice.Status.PARTIALLY_PAID
        else:
            self.status = Invoice.Status.DRAFT
        Invoice.objects.filter(pk=self.pk).update(status=self.status)

    @property
    def total_amount(self):
        return sum(item.amount for item in self.items.all())

    @property
    def paid_amount(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def outstanding_amount(self):
        return max(self.total_amount - self.paid_amount, 0)


class InvoiceItem(models.Model):
    invoice        = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description    = models.CharField(max_length=255)
    amount         = models.DecimalField(max_digits=10, decimal_places=2)

    # Generic link back to any module
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id      = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.description} – {self.amount}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'CASH', 'Cash'
        CARD = 'CARD', 'Card'
        UPI  = 'UPI',  'UPI'

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    method          = models.CharField(max_length=10, choices=Method.choices)
    reference_no    = models.CharField(max_length=100, blank=True)
    paid_at         = models.DateTimeField(auto_now_add=True)
    processed_by    = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.invoice.invoice_number} – {self.amount} ({self.method})"