from django.urls import path
from .views import health_check

app_name = "consultations"

urlpatterns = [
    path("ping/", health_check, name="ping"),
]