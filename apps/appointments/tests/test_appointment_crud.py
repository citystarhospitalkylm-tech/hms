# apps/appointments/tests/test_appointment_crud.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.appointments.models import Appointment
from apps.patients.models import Patient
from apps.core.models import Role, User
from django.contrib.auth.models import Permission
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def doctor_role(db):
    perms = Permission.objects.filter(
        codename__in=[
            "view_appointment",
            "add_appointment",
            "change_appointment",
            "delete_appointment",
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
class TestAppointmentAPI:
    def test_book_and_list(self, api_client, doctor_user):
        api_client.force_authenticate(doctor_user)
        patient = Patient.objects.create(
            first_name="Alice", last_name="Smith", dob="1980-05-05",
            gender="F", blood_group="A+"
        )
        url = reverse("appointment-list")
        data = {
            "patient": patient.id,
            "doctor": doctor_user.id,
            "appointment_time": timezone.now().isoformat(),
        }
        resp = api_client.post(url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["token_number"] == 1

        list_resp = api_client.get(url)
        assert list_resp.status_code == status.HTTP_200_OK
        assert len(list_resp.data) == 1

    def test_double_book_conflict(self, api_client, doctor_user):
        api_client.force_authenticate(doctor_user)
        patient = Patient.objects.create(
            first_name="Bob", last_name="Lee", dob="1975-08-08",
            gender="M", blood_group="B+"
        )
        time = timezone.now()
        Appointment.objects.create(
            patient=patient, doctor=doctor_user,
            appointment_time=time, created_by=doctor_user
        )
        resp = api_client.post(reverse("appointment-list"), {
            "patient": patient.id,
            "doctor": doctor_user.id,
            "appointment_time": time.isoformat()
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_permission_denied(self, api_client, db):
        role = Role.objects.create(name="Receptionist")
        user = User.objects.create_user(
            username="rec", password="pass123", role=role
        )
        api_client.force_authenticate(user)
        resp = api_client.get(reverse("appointment-list"))
        assert resp.status_code == status.HTTP_403_FORBIDDEN