from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    MedicineViewSet, BatchViewSet,
    PharmacySaleViewSet, SaleItemViewSet
)

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'batches',   BatchViewSet)
router.register(r'sales',     PharmacySaleViewSet)
router.register(r'sale-items', SaleItemViewSet, basename='saleitem')

urlpatterns = [
    path('pharmacy/', include(router.urls)),
]