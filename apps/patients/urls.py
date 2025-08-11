from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Lazy import inside a function to avoid premature model evaluation
def get_patient_viewset():
    from .views import PatientViewSet
    return PatientViewSet

router.register(r"patients", get_patient_viewset(), basename="patient")

urlpatterns = router.urls