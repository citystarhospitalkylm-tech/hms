from rest_framework import generics
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import AppointmentPermission


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset           = Appointment.objects.all()
    serializer_class   = AppointmentSerializer
    permission_classes = [AppointmentPermission]


class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field       = 'id'
    queryset           = Appointment.objects.all()
    serializer_class   = AppointmentSerializer
    permission_classes = [AppointmentPermission]