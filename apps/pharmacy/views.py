from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from .models import Supplier, DrugCategory, Drug, Batch, SaleItem
from .serializers import (
    SupplierSerializer,
    DrugCategorySerializer,
    DrugSerializer,
    SaleItemSerializer,
    StockSerializer,
)
from django.shortcuts import render
from config.rbac import require_module

@require_module("pharmacy")
def pharmacy_dashboard(request):
    return render(request, "pharmacy/dashboard.html")
# 🔐 Role-based permission
class IsPharmacistOrAdmin(BasePermission):
    """
    Allows access only to users with role 'pharmacist' or 'admin'.
    Assumes user has a related profile with a 'role' attribute.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            hasattr(user, 'profile') and
            user.profile.role in ['pharmacist', 'admin']
        )

# 📦 ViewSets with permission applied
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsPharmacistOrAdmin]

class DrugCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrugCategory.objects.all()
    serializer_class = DrugCategorySerializer
    permission_classes = [IsPharmacistOrAdmin]

class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.select_related("category").all()
    serializer_class = DrugSerializer
    permission_classes = [IsPharmacistOrAdmin]

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.select_related("batch__drug").all()
    serializer_class = SaleItemSerializer
    permission_classes = [IsPharmacistOrAdmin]

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Batch.objects.select_related("drug", "supplier").all()
    serializer_class = StockSerializer
    permission_classes = [IsPharmacistOrAdmin]