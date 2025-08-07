from rest_framework import viewsets, permissions
from .models import Ward, Bed, Admission, Discharge, VitalSign
from .serializers import (
    WardSerializer, BedSerializer,
    AdmissionSerializer, DischargeSerializer,
    VitalSignSerializer
)
from .permissions import IsIPDStaffOrReadOnly

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.IsAuthenticated, IsIPDStaffOrReadOnly]

class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.select_related('ward').all()
    serializer_class = BedSerializer
    permission_classes = [permissions.IsAuthenticated, IsIPDStaffOrReadOnly]

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.select_related('patient','ward','bed').all()
    serializer_class = AdmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsIPDStaffOrReadOnly]

class DischargeViewSet(viewsets.ModelViewSet):
    queryset = Discharge.objects.select_related('admission').all()
    serializer_class = DischargeSerializer
    permission_classes = [permissions.IsAuthenticated, IsIPDStaffOrReadOnly]

class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.select_related('admission').all()
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated, IsIPDStaffOrReadOnly]