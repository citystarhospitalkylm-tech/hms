from rest_framework import viewsets
from .models import Supplier, DrugCategory, Drug, Batch, SaleItem
from .serializers import (
    SupplierSerializer,
    DrugCategorySerializer,
    DrugSerializer,
    SaleItemSerializer,
    StockSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class DrugCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrugCategory.objects.all()
    serializer_class = DrugCategorySerializer


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.select_related("category").all()
    serializer_class = DrugSerializer


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.select_related("batch__drug").all()
    serializer_class = SaleItemSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Batch.objects.select_related("drug", "supplier").all()
    serializer_class = StockSerializer