from rest_framework import permissions
from apps.users.models import User


class AppointmentPermission(permissions.BasePermission):
    """
    SAFE_METHODS: any authenticated user
    POST/PUT/PATCH: receptionist or admin
    DELETE: admin only
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('POST', 'PUT', 'PATCH'):
            return user.role in (User.Roles.RECEPTIONIST, User.Roles.ADMIN)

        if request.method == 'DELETE':
            return user.role == User.Roles.ADMIN

        return False