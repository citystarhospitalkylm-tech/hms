from rest_framework import permissions
from apps.security.models import User


class BillingPermission(permissions.BasePermission):
    """
    Only Admin and Receptionist can view or mutate billing data.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated
            and user.role in (User.Roles.ADMIN, User.Roles.RECEPTIONIST)
        )