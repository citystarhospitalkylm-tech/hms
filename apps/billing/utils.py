from django.utils import timezone
from .models import Invoice
from django.core.mail import send_mail

def send_overdue_reminders():
    today = timezone.now().date()
    overdue = Invoice.objects.filter(status=Invoice.Status.OVERDUE, due_date__lt=today)
    for inv in overdue:
        # Hook: integrate with email/SMS gateway
        send_mail(
            subject=f"Invoice {inv.invoice_number} Overdue",
            message=f"Dear {inv.patient.first_name}, your invoice {inv.invoice_number} is overdue by {today - inv.due_date} days. Outstanding: {inv.outstanding_amount}.",
            from_email='hospital@noreply.local',
            recipient_list=[inv.patient.email],
            fail_silently=True,
        )