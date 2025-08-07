# apps/labs/tests/test_laborder_crud.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.core.models import Role
from django.contrib.auth.models import Permission
from apps.patients.models import Patient
from .models import LabTest, LabOrder

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def order_role(db):
    perms = Permission.objects.filter(
        codename__in=[
            "view_laborder", "add_laborder",
            "change_laborder", "delete_laborder",
        ]
    )
    role = Role.objects.create(name="LabUser")
    role.permissions.set(perms)
    return role


@pytest.fixture
def order_user(order_role, db):
    user = User.objects.create_user("labtech", "pw", role=order_role)
    return user


@pytest.mark.django_db
class TestLabOrderAPI:
    def test_order_and_list(self, api_client, order_user):
        api_client.force_authenticate(order_user)
        patient = Patient.objects.create(
            first_name="Ann", last_name="Lee", dob="1990-01-01",
            gender="F", blood_group="O+"
        )
        test = LabTest.objects.create(code="LIP", name="Lipid Panel", price="350.00")
        url = reverse("laborder-list")
        data = {"patient": patient.id, "doctor": order_user.id, "test": test.id}
        resp = api_client.post(url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["status"] == "ORDERED"

        list_resp = api_client.get(url)
        assert list_resp.status_code == status.HTTP_200_OK
        assert len(list_resp.data) == 1

    def test_cancel_order(self, api_client, order_user):
        api_client.force_authenticate(order_user)
        patient = Patient.objects.create(
            first_name="Tom", last_name="Ray", dob="1985-03-03",
            gender="M", blood_group="B+"
        )
        test = LabTest.objects.create(code="GLU", name="Glucose", price="100.00")
        order = LabOrder.objects.create(
            patient=patient, doctor=order_user, test=test, created_by=order_user
        )
        url = reverse("laborder-detail", args=(order.id,))
        resp = api_client.patch(url, {"status": "CANCELLED"})
        assert resp.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == "CANCELLED"