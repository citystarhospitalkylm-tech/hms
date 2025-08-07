# apps/labs/permissions.py

from rest_framework import permissions


class LabTestPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["labs.view_labtest"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["labs.add_labtest"],
        "PUT": ["labs.change_labtest"],
        "PATCH": ["labs.change_labtest"],
        "DELETE": ["labs.delete_labtest"],
    }


class LabOrderPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["labs.view_laborder"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["labs.add_laborder"],
        "PUT": ["labs.change_laborder"],
        "PATCH": ["labs.change_laborder"],
        "DELETE": ["labs.delete_laborder"],
    }