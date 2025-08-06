from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    InvoiceViewSet, InvoiceItemViewSet, PaymentViewSet, DailyCashReportView
)

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'items', InvoiceItemViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('billing/', include(router.urls)),
    path('billing/reports/daily-cash/', DailyCashReportView.as_view(), name='daily-cash-report'),
]