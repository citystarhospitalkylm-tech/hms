# apps/appointments/permissions.py

from rest_framework import permissions


class AppointmentPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["appointments.view_appointment"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["appointments.add_appointment"],
        "PUT": ["appointments.change_appointment"],
        "PATCH": ["appointments.change_appointment"],
        "DELETE": ["appointments.delete_appointment"],
    }