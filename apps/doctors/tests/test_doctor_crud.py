# apps/doctors/tests/test_doctor_crud.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.doctors.models import Doctor
from django.contrib.auth import get_user_model
from apps.core.models import Role
from django.contrib.auth.models import Permission

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def doctor_role(db):
    perms = Permission.objects.filter(
        codename__in=[
            "view_doctor",
            "add_doctor",
            "change_doctor",
            "delete_doctor",
        ]
    )
    role = Role.objects.create(name="DoctorRole")
    role.permissions.set(perms)
    return role


@pytest.fixture
def doctor_user(doctor_role, db):
    user = User.objects.create_user(
        username="drjohn", password="secure", role=doctor_role
    )
    return user


@pytest.mark.django_db
class TestDoctorAPI:

    def test_create_and_list_doctor(self, api_client, doctor_user):
        api_client.force_authenticate(doctor_user)
        # Prepare another user to become a doctor profile
        u2 = User.objects.create_user(
            username="drjane", password="pass123", role=doctor_user.role
        )
        url = reverse("doctor-list")
        payload = {
            "user_id": u2.id,
            "specialty": "Cardiology",
            "qualifications": "MD, FACC",
            "phone": "123-456-7890",
            "department": "Cardiology",
            "status": "ACTIVE",
        }
        resp = api_client.post(url, payload)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["specialty"] == "Cardiology"

        list_resp = api_client.get(url)
        assert list_resp.status_code == status.HTTP_200_OK
        assert any(d["user"]["username"] == "drjane" for d in list_resp.data)

    def test_update_status(self, api_client, doctor_user):
        api_client.force_authenticate(doctor_user)
        # Create profile
        u3 = User.objects.create_user(
            username="dralex", password="pass123", role=doctor_user.role
        )
        doc = Doctor.objects.create(
            user=u3, specialty="Neurology", created_by=doctor_user
        )
        url = reverse("doctor-detail", args=(doc.id,))
        resp = api_client.patch(url, {"status": "SUSPENDED"})
        assert resp.status_code == status.HTTP_200_OK
        assert Doctor.objects.get(id=doc.id).status == "SUSPENDED"

    def test_permission_denied(self, api_client, db):
        # A user without doctor perms
        role = Role.objects.create(name="Nurse")
        user = User.objects.create_user(
            username="nurse", password="pwd", role=role
        )
        api_client.force_authenticate(user)
        resp = api_client.get(reverse("doctor-list"))
        assert resp.status_code == status.HTTP_403_FORBIDDEN