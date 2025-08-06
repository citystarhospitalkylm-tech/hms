from rest_framework import viewsets
from .models import Medicine, Batch, PharmacySale, SaleItem
from .serializers import (
    MedicineSerializer, BatchSerializer,
    PharmacySaleSerializer, SaleItemSerializer
)
from .permissions import PharmacyPermission


class MedicineViewSet(viewsets.ModelViewSet):
    queryset           = Medicine.objects.all()
    serializer_class   = MedicineSerializer
    permission_classes = [PharmacyPermission]


class BatchViewSet(viewsets.ModelViewSet):
    queryset           = Batch.objects.select_related('medicine').all()
    serializer_class   = BatchSerializer
    permission_classes = [PharmacyPermission]


class PharmacySaleViewSet(viewsets.ModelViewSet):
    queryset           = PharmacySale.objects.select_related('patient','sold_by').all()
    serializer_class   = PharmacySaleSerializer
    permission_classes = [PharmacyPermission]


class SaleItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = SaleItem.objects.select_related('sale','medicine','batch').all()
    serializer_class   = SaleItemSerializer
    permission_classes = [PharmacyPermission]