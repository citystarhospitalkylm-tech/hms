# core/rbac.py
from functools import wraps
from typing import Set
from django.conf import settings
from django.http import HttpResponseForbidden

# 1) Central mapping: role -> allowed modules
ROLE_MODULES = {
    "admin": [
        "appointments", "billing", "consultation", "doctor",
        "inventory", "ipd", "labs", "patients",
        "pharmacy", "security", "users",
    ],
    "doctor": [
        "appointments", "consultation", "patients", "labs",
    ],
    "nurse": [
        "patients", "ipd", "labs", "pharmacy",
    ],
    "reception": [
        "appointments", "billing", "patients",
    ],
}

# 2) Demo toggle (put RBAC_DEMO_UNLOCK=True in settings to unlock everything)
DEMO_UNLOCK = getattr(settings, "RBAC_DEMO_UNLOCK", False)

def _norm(s: str) -> str:
    return (s or "").strip().lower()

def get_user_roles(user) -> Set[str]:
    if not getattr(user, "is_authenticated", False):
        return set()
    roles = { _norm(name) for name in user.groups.values_list("name", flat=True) }
    if getattr(user, "is_superuser", False):
        roles.add("admin")
    return roles

def get_all_modules() -> Set[str]:
    out = set()
    for mods in ROLE_MODULES.values():
        out.update(map(_norm, mods))
    return out

def get_allowed_modules(user) -> Set[str]:
    if DEMO_UNLOCK:
        return get_all_modules()
    allowed = set()
    for role in get_user_roles(user):
        allowed.update(map(_norm, ROLE_MODULES.get(role, [])))
    return allowed

def has_module_access(user, module: str) -> bool:
    return _norm(module) in get_allowed_modules(user)

def require_module(module: str):
    """
    Decorator for any view inside a module.
    Example:
        @require_module("billing")
        def billing_dashboard(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, "user", None)
            if not (user and user.is_authenticated):
                # Defer to your configured login URL
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if not has_module_access(user, module):
                return HttpResponseForbidden("No permission for this module")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator