from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer
from .permissions import PatientAccessPermission


class PatientListCreateView(generics.ListCreateAPIView):
    queryset           = Patient.objects.all().order_by('-created_at')
    serializer_class   = PatientSerializer
    permission_classes = [PatientAccessPermission]


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field       = 'id'
    queryset           = Patient.objects.all()
    serializer_class   = PatientSerializer
    permission_classes = [PatientAccessPermission]