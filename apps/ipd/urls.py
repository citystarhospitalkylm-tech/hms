from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    WardViewSet, RoomViewSet, BedViewSet, AdmissionViewSet,
    VitalSignViewSet, NursingNoteViewSet, RoundViewSet,
    ServiceUsageViewSet, DischargeSummaryViewSet
)

router = DefaultRouter()
router.register(r'wards', WardViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'beds', BedViewSet)
router.register(r'admissions', AdmissionViewSet)
router.register(r'vitals', VitalSignViewSet)
router.register(r'nursing-notes', NursingNoteViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'services', ServiceUsageViewSet)
router.register(r'discharges', DischargeSummaryViewSet)

urlpatterns = [
    path('ipd/', include(router.urls)),
]