from rest_framework import viewsets
from .models import Consultation, Prescription, Referral
from .serializers import (
    ConsultationSerializer, PrescriptionSerializer, ReferralSerializer
)
from .permissions import ConsultationPermission

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset           = Consultation.objects.select_related('patient','doctor').all()
    serializer_class   = ConsultationSerializer
    permission_classes = [ConsultationPermission]
    basename           = 'consultation'

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset           = Prescription.objects.select_related('consultation').all()
    serializer_class   = PrescriptionSerializer
    permission_classes = [ConsultationPermission]
    basename           = 'prescription'

class ReferralViewSet(viewsets.ModelViewSet):
    queryset           = Referral.objects.select_related('consultation').all()
    serializer_class   = ReferralSerializer
    permission_classes = [ConsultationPermission]
    basename           = 'referral'