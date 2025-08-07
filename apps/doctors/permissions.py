# apps/doctors/permissions.py

from rest_framework import permissions


class DoctorPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["doctors.view_doctor"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["doctors.add_doctor"],
        "PUT": ["doctors.change_doctor"],
        "PATCH": ["doctors.change_doctor"],
        "DELETE": ["doctors.delete_doctor"],
    }