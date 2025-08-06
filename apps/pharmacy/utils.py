from django.utils import timezone
from .models import Medicine

def get_low_stock_alerts():
    """
    Return list of medicines where total_stock <= low_stock_threshold or
    batches expiring within 30 days.
    """
    alerts = []
    today = timezone.now().date()
    for med in Medicine.objects.all():
        if med.total_stock <= med.low_stock_threshold:
            alerts.append({
                'medicine': med.name,
                'issue': 'Low stock',
                'quantity': med.total_stock
            })
        for batch in med.batches.filter(expiry_date__lte=today + timezone.timedelta(days=30)):
            alerts.append({
                'medicine': med.name,
                'batch': batch.batch_number,
                'issue': f'Expiring on {batch.expiry_date}'
            })
    return alerts