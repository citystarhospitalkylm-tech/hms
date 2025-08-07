from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    WardViewSet, BedViewSet,
    AdmissionViewSet, DischargeViewSet,
    VitalSignViewSet
)

router = DefaultRouter()
router.register(r'wards', WardViewSet, basename='ward')
router.register(r'beds', BedViewSet, basename='bed')
router.register(r'admissions', AdmissionViewSet, basename='admission')
router.register(r'discharges', DischargeViewSet, basename='discharge')
router.register(r'vitalsigns', VitalSignViewSet, basename='vitalsign')

urlpatterns = [
    path('api/ipd/', include(router.urls)),
]