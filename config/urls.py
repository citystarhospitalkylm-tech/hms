from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import whoami
from apps.security.views import home
# from apps.security.views import login_view  # Optional custom login
from public.views import landing_page
from django.contrib.auth import views as auth_views

app_name = "security"

urlpatterns = [
    # Admin & debug
    path("admin/", admin.site.urls),
    path("whoami/", whoami),

    # Public landing page
    path("", landing_page, name="landing"),

    # Authentication
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout"
    ),
    # If you want to use your own login view instead:
    # path("login/", login_view, name="login"),

    # Core modules
    path("", include(("public.urls", "public"), namespace="public")),
    path("home/", home),

    path("api/patients/", include("apps.patients.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
    path("api/consultations/", include("apps.consultations.urls")),
    path("api/pharmacy/", include("apps.pharmacy.urls")),
    path("api/billing/", include("apps.billing.urls")),
    path("api/ipd/", include("apps.ipd.urls")),
    # path("api/reports/", include("apps.reports.urls")),

    # Optional modules
    path("accounts/", include("security.urls", namespace="security_accounts")),
    path("api/v1/security/", include("apps.security.urls", namespace="security_api")),

    # Uncomment if user/role management is restored
    # path("api/accounts/", include("apps.accounts.user_urls")),
    # path("api/auth/", include("accounts.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)