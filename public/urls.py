from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("login/<str:role>/", views.role_login, name="role_login"),

    # Locked dashboards
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/nurse/", views.nurse_dashboard, name="nurse_dashboard"),
    path("dashboard/pharmacy/", views.pharmacy_dashboard, name="pharmacy_dashboard"),
    path("dashboard/lab/", views.lab_dashboard, name="lab_dashboard"),
    path("dashboard/appointments/", views.appointments_dashboard, name="appointments_dashboard"),
    path("dashboard/billing/", views.billing_dashboard, name="billing_dashboard"),
    path("dashboard/consultations/", views.consultations_dashboard, name="consultations_dashboard"),
]