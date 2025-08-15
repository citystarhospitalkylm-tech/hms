from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    login_view,
    LogoutView,
    PasswordChangeView,
    UserProfileView,
    RoleViewSet,
    PermissionViewSet,
)

app_name = "security"

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"permissions", PermissionViewSet, basename="permission")

urlpatterns = [
    # JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Session / Password
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "auth/password/change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),

    # Profile
    path("me/", UserProfileView.as_view(), name="user_profile"),

    # RBAC
    path("", include(router.urls)),
]