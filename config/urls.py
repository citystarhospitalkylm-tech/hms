from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.security.views import home
from apps.security.views import login_view  # ✅ Corrected import
from public.views import landing_page        # ✅ Added landing page

app_name = "security"

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public landing page
    path('', landing_page, name='landing'),

    # Core modules
    path("", include(("public.urls", "public"), namespace="public")),
    path('home/', home),
    path('login/', login_view, name='login'),
    path("api/patients/", include("apps.patients.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
    path("api/consultations/", include("apps.consultations.urls")),
    path("api/pharmacy/", include("apps.pharmacy.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/ipd/", include("apps.ipd.urls")),
    # path("api/reports/", include("apps.reports.urls")),

    # Optional modules
    path('accounts/', include('security.urls', namespace='security')),
    path("api/v1/security/", include("apps.security.urls", namespace="security")),

    # Uncomment if user/role management is restored
    # path("api/accounts/", include("apps.accounts.user_urls")),
    # path("api/auth/", include("accounts.urls")),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)