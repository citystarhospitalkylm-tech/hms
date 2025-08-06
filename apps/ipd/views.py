from rest_framework import viewsets
from rest_framework.decorators import action
from .models import (
    Ward, Room, Bed, Admission, VitalSign,
    NursingNote, Round, ServiceUsage, DischargeSummary
)
from .serializers import (
    WardSerializer, RoomSerializer, BedSerializer,
    AdmissionSerializer, VitalSignSerializer,
    NursingNoteSerializer, RoundSerializer,
    ServiceUsageSerializer, DischargeSummarySerializer
)
from .permissions import IPDBasePermission


class WardViewSet(viewsets.ModelViewSet):
    queryset         = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [IPDBasePermission]
    basename = 'ward'


class RoomViewSet(viewsets.ModelViewSet):
    queryset         = Room.objects.select_related('ward').all()
    serializer_class = RoomSerializer
    permission_classes = [IPDBasePermission]
    basename = 'room'


class BedViewSet(viewsets.ModelViewSet):
    queryset         = Bed.objects.select_related('room').all()
    serializer_class = BedSerializer
    permission_classes = [IPDBasePermission]
    basename = 'bed'


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset         = Admission.objects.select_related('patient','bed').all()
    serializer_class = AdmissionSerializer
    permission_classes = [IPDBasePermission]
    basename = 'admission'


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset         = VitalSign.objects.select_related('admission').all()
    serializer_class = VitalSignSerializer
    permission_classes = [IPDBasePermission]
    basename = 'vitals'


class NursingNoteViewSet(viewsets.ModelViewSet):
    queryset         = NursingNote.objects.select_related('admission').all()
    serializer_class = NursingNoteSerializer
    permission_classes = [IPDBasePermission]
    basename = 'nursingnote'


class RoundViewSet(viewsets.ModelViewSet):
    queryset         = Round.objects.select_related('admission').all()
    serializer_class = RoundSerializer
    permission_classes = [IPDBasePermission]
    basename = 'round'


class ServiceUsageViewSet(viewsets.ModelViewSet):
    queryset         = ServiceUsage.objects.select_related('admission').all()
    serializer_class = ServiceUsageSerializer
    permission_classes = [IPDBasePermission]
    basename = 'serviceusage'


class DischargeSummaryViewSet(viewsets.ModelViewSet):
    queryset         = DischargeSummary.objects.select_related('admission').all()
    serializer_class = DischargeSummarySerializer
    permission_classes = [IPDBasePermission]
    basename = 'dischargesummary'