from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SupplierViewSet, DrugCategoryViewSet, DrugViewSet,
    StockViewSet, PrescriptionViewSet, DispenseViewSet
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'categories', DrugCategoryViewSet)
router.register(r'drugs', DrugViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'dispensations', DispenseViewSet)

urlpatterns = [
    path('api/pharmacy/', include(router.urls)),
]