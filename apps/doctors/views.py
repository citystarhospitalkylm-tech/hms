# apps/doctors/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Doctor
from .serializers import DoctorSerializer
from .permissions import DoctorPermissions


class DoctorViewSet(viewsets.ModelViewSet):
    """
    CRUD for Doctor Profiles.
    """
    queryset = Doctor.objects.select_related("user")
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, DoctorPermissions]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "department", "specialty"]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "specialty",
        "department",
    ]
    ordering_fields = ["user__last_name", "specialty"]
    ordering = ["user__last_name"]