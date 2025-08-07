# apps/labs/urls.py

from rest_framework.routers import DefaultRouter
from .views import LabTestViewSet, LabOrderViewSet

router = DefaultRouter()
router.register(r"lab-tests", LabTestViewSet, basename="labtest")
router.register(r"lab-orders", LabOrderViewSet, basename="laborder")

urlpatterns = router.urls