# apps/patients/tests/test_patient_crud.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.patients.models import Patient
from apps.core.models import Role, User
from django.contrib.auth.models import Permission


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def doctor_role(db):
    perms = Permission.objects.filter(
        codename__in=[
            "view_patient",
            "add_patient",
            "change_patient",
            "delete_patient",
        ]
    )
    role = Role.objects.create(name="Doctor")
    role.permissions.set(perms)
    return role


@pytest.fixture
def doctor_user(doctor_role, db):
    user = User.objects.create_user(
        username="doc", password="pass123", role=doctor_role
    )
    return user


@pytest.mark.django_db
class TestPatientAPI:
    def test_create_and_list(self, api_client, doctor_user):
        api_client.force_authenticate(doctor_user)
        url = reverse("patient-list")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "dob": "1990-01-01",
            "gender": "M",
            "blood_group": "O+",
        }
        resp = api_client.post(url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert "mrn" in resp.data

        list_resp = api_client.get(url)
        assert list_resp.status_code == status.HTTP_200_OK
        assert len(list_resp.data) == 1

    def test_permission_denied(self, api_client, db):
        role = Role.objects.create(name="Receptionist")
        user = User.objects.create_user(
            username="rec", password="pass123", role=role
        )
        api_client.force_authenticate(user)
        url = reverse("patient-list")
        resp = api_client.get(url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN