# apps/patients/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .serializers import PatientSerializer
from .permissions import PatientPermissions


class PatientViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoint for Patients with search, filter, and ordering.
    """
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, PatientPermissions]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["gender", "blood_group"]
    search_fields = ["first_name", "last_name", "mrn", "phone_number"]
    ordering_fields = ["created_at", "first_name", "last_name", "dob"]
    ordering = ["-created_at"]