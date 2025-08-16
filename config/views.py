# core/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .rbac import get_user_roles, get_allowed_modules

@login_required
def whoami(request):
    roles = sorted(get_user_roles(request.user))
    modules = sorted(get_allowed_modules(request.user))
    return JsonResponse({
        "user": request.user.username,
        "roles": roles,
        "allowed_modules": modules,
        "demo_unlock": getattr(settings, "RBAC_DEMO_UNLOCK", False),
        "is_superuser": request.user.is_superuser,
        "is_staff": request.user.is_staff,
    })