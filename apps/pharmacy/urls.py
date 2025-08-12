from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet,
    DrugCategoryViewSet,
    DrugViewSet,
    SaleItemViewSet,
    StockViewSet,
)

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"drug-categories", DrugCategoryViewSet, basename="drugcategory")
router.register(r"drugs", DrugViewSet, basename="drug")
router.register(r"sale-items", SaleItemViewSet, basename="saleitem")
router.register(r"stock", StockViewSet, basename="stock")

urlpatterns = router.urls