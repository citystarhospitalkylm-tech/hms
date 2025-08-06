from rest_framework import permissions
from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Roles.ADMIN
        )


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Roles.DOCTOR
        )


# Repeat similar classes for Receptionist, Pharmacy, LabTech, Accountant, Inventory, HR...