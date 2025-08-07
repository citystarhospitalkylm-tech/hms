# apps/appointments/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import AppointmentPermissions


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    CRUD + calendar endpoint for Appointments.
    """
    queryset = Appointment.objects.select_related("patient", "doctor")
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, AppointmentPermissions]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "doctor", "appointment_time"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "token_number",
    ]
    ordering_fields = ["appointment_time", "token_number"]
    ordering = ["appointment_time"]