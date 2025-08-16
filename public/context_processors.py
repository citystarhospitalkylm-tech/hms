# public/context_processors.py
from .views import ROLES, ROLE_REDIRECTS

def role_nav(request):
    return {
        "roles": ROLES,
        "ROLE_REDIRECTS": ROLE_REDIRECTS,
    }