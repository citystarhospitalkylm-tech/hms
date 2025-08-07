from rest_framework import permissions

class IsPharmacistOrReadOnly(permissions.BasePermission):
    """
    Write permissions only for users in the 'Pharmacists' group.
    Read-only for everyone else.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Pharmacists').exists()