# apps/labs/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import LabTest, LabOrder
from .serializers import LabTestSerializer, LabOrderSerializer
from .permissions import LabTestPermissions, LabOrderPermissions
from django.shortcuts import render
from config.rbac import require_module

@require_module("labs")
def labs_dashboard(request):
    return render(request, "labs/dashboard.html")

class LabTestViewSet(viewsets.ModelViewSet):
    """
    CRUD for lab test catalog.
    """
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated, LabTestPermissions]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["code", "name"]
    ordering_fields = ["code", "name"]
    ordering = ["code"]


class LabOrderViewSet(viewsets.ModelViewSet):
    """
    CRUD for lab orders.
    """
    queryset = LabOrder.objects.select_related("patient", "test", "doctor")
    serializer_class = LabOrderSerializer
    permission_classes = [IsAuthenticated, LabOrderPermissions]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "test", "doctor", "ordered_at"]
    search_fields = ["patient__first_name", "patient__last_name", "test__name"]
    ordering_fields = ["ordered_at", "status"]
    ordering = ["-ordered_at"]