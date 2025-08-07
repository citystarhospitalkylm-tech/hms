from rest_framework import permissions

class IsIPDStaffOrReadOnly(permissions.BasePermission):
    """
    Nurses can record vitals; doctors can admit/discharge;
    read-only for others.
    """
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.basename == 'vitalsign':
            return user.groups.filter(name='Nurses').exists()
        if view.basename in ('admission','discharge'):
            return user.groups.filter(name__in=['Doctors','Admins']).exists()
        return False