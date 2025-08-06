from rest_framework import permissions
from apps.users.models import User


class IPDBasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # SAFE methods for all authenticated
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admin always allowed
        if user.role == User.Roles.ADMIN:
            return True

        # Create admission: receptionist or nurse
        if view.basename == 'admission-list' and request.method == 'POST':
            return user.role in (User.Roles.RECEPTIONIST, User.Roles.INVENTORY)

        # Create vitals/note/service: nurse
        if view.basename in ('vitals-list','nursingnote-list','serviceusage-list') and request.method == 'POST':
            return user.role == User.Roles.PHARMACY or user.role == User.Roles.RECEPTIONIST or user.role == User.Roles.LAB_TECH or user.role == User.Roles.DOCTOR or user.role == User.Roles.RECEPTIONIST or user.role == User.Roles.INVENTORY or user.role == User.Roles.HR or user.role == User.Roles.PHARMACY # Replace with correct roles
        # Create round/discharge: doctor
        if view.basename in ('round-list','dischargesummary-list') and request.method == 'POST':
            return user.role == User.Roles.DOCTOR

        # Updates/deletes only admin
        return False