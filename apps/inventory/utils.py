from django.utils import timezone
from datetime import timedelta
from .models import StockChange

def get_stock_drop_alerts(hours=24):
    """
    Returns medicines whose total stock change in the last `hours` is negative.
    """
    since     = timezone.now() - timedelta(hours=hours)
    alerts    = []
    # aggregate deltas per medicine
    changes = (
        StockChange.objects
        .filter(timestamp__gte=since)
        .values('medicine__id', 'medicine__name')
        .annotate(net_delta=models.Sum('delta'))
        .filter(net_delta__lt=0)
    )

    for entry in changes:
        alerts.append({
            'medicine_id': entry['medicine__id'],
            'medicine': entry['medicine__name'],
            'net_change': entry['net_delta'],
            'period_hours': hours,
            'issue': 'Stock dropped'
        })

    return alerts