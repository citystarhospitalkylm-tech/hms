from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Supplier, DrugCategory, Drug, Stock,
    Prescription, Dispense
)
from .serializers import (
    SupplierSerializer, DrugCategorySerializer, DrugSerializer,
    StockSerializer, PrescriptionSerializer, DispenseSerializer
)
from .permissions import IsPharmacistOrReadOnly

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacistOrReadOnly]

class DrugCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrugCategory.objects.all()
    serializer_class = DrugCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacistOrReadOnly]

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.select_related('category').all()
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacistOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'unit_price']

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('drug', 'supplier').all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacistOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['drug', 'batch_no', 'expiry_date']
    ordering_fields = ['received_at', 'expiry_date']

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.prefetch_related('items').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'prescribed_by']

class DispenseViewSet(viewsets.ModelViewSet):
    queryset = Dispense.objects.select_related('prescription_item__drug').all()
    serializer_class = DispenseSerializer
    permission_classes = [permissions.IsAuthenticated]