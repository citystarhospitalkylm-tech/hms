# security/decorators.py
from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles):
    def check_role(u):
        return u.is_authenticated and u.role in allowed_roles
    return user_passes_test(
    check_role,
    login_url='/unauthorized/',  # or reverse('unauthorized')
    redirect_field_name=None     # disables ?next= param
)
