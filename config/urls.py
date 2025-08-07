from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),       # token endpoints
    path("api/accounts/", include("accounts.user_urls")),  # user/role management
    path("api/patients/", include("patients.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/consultations/", include("consultations.urls")),
    path("api/pharmacy/", include("pharmacy.urls")),
    path("api/billing/", include("billing.urls")),
    path("api/ipd/", include("ipd.urls")),
    path("api/reports/", include("reports.urls")),
    # security endpoints (optional dashboard)
    path("api/security/", include("security.urls")),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)