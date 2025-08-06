from django.urls import path
from .views import PatientListCreateView, PatientRetrieveUpdateDestroyView

urlpatterns = [
    path('patients/',           PatientListCreateView.as_view(),           name='patient-list-create'),
    path('patients/<uuid:id>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-detail'),
]