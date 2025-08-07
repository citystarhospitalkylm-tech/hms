# apps/patients/permissions.py

from rest_framework import permissions


class PatientPermissions(permissions.DjangoModelPermissions):
    """
    Map HTTP methods to custom 'patients' app permissions.
    """
    perms_map = {
        "GET": ["patients.view_patient"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["patients.add_patient"],
        "PUT": ["patients.change_patient"],
        "PATCH": ["patients.change_patient"],
        "DELETE": ["patients.delete_patient"],
    }