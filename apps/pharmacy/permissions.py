from rest_framework import permissions
from apps.users.models import User


class PharmacyPermission(permissions.BasePermission):
    """
    SAFE_METHODS: any authenticated user
    POST: pharmacist or admin
    DELETE/PUT/PATCH: admin only
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return user.role in (User.Roles.PHARMACY, User.Roles.ADMIN)

        return user.role == User.Roles.ADMIN