# apps/consultations/views.py

from django.http import JsonResponse
from rest_framework import viewsets
from .models import Consultation, Prescription, Referral
from .serializers import (
    ConsultationSerializer,
    PrescriptionSerializer,
    ReferralSerializer
)
from .permissions import ConsultationPermission
from django.shortcuts import render
from config.rbac import require_module
from django.shortcuts import render
from config.rbac import require_module

@require_module("doctor")
def doctor_dashboard(request):
    return render(request, "doctor/dashboard.html")
@require_module("consultation")
def consultation_dashboard(request):
    return render(request, "consultation/dashboard.html")

def health_check(request):
    """
    Simple endpoint to verify the consultations module is up.
    """
    return JsonResponse({"status": "consultations module active"})


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    CRUD for Consultation. 
    """
    queryset = (
        Consultation.objects
        .select_related("patient", "doctor")
        .prefetch_related("referrals", "prescriptions__items")
        .all()
    )
    serializer_class = ConsultationSerializer
    permission_classes = [ConsultationPermission]


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    CRUD for Prescription and its nested items.
    """
    queryset = (
        Prescription.objects
        .select_related("consultation", "patient", "prescribed_by")
        .prefetch_related("items")
        .all()
    )
    serializer_class = PrescriptionSerializer
    permission_classes = [ConsultationPermission]


class ReferralViewSet(viewsets.ModelViewSet):
    """
    CRUD for Referral records tied to a Consultation.
    """
    queryset = (
        Referral.objects
        .select_related("consultation", "referred_by")
        .all()
    )
    serializer_class = ReferralSerializer
    permission_classes = [ConsultationPermission]