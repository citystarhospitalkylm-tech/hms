# apps/labs/tests/test_labtest_crud.py

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.core.models import Role
from django.contrib.auth.models import Permission
from .models import LabTest

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def lab_role(db):
    perms = Permission.objects.filter(
        codename__in=[
            "view_labtest", "add_labtest",
            "change_labtest", "delete_labtest",
        ]
    )
    role = Role.objects.create(name="LabManager")
    role.permissions.set(perms)
    return role


@pytest.fixture
def lab_user(lab_role, db):
    user = User.objects.create_user("labuser", "pw", role=lab_role)
    return user


@pytest.mark.django_db
class TestLabTestAPI:
    def test_create_and_list(self, api_client, lab_user):
        api_client.force_authenticate(lab_user)
        url = reverse("labtest-list")
        payload = {"code": "CBC", "name": "Complete Blood Count", "price": "200.00"}
        resp = api_client.post(url, payload)
        assert resp.status_code == status.HTTP_201_CREATED
        assert LabTest.objects.filter(code="CBC").exists()

        list_resp = api_client.get(url)
        assert list_resp.status_code == status.HTTP_200_OK
        assert any(t["code"] == "CBC" for t in list_resp.data)

    def test_permission_denied(self, api_client, db):
        role = Role.objects.create(name="Intern")
        user = User.objects.create_user("int", "pw", role=role)
        api_client.force_authenticate(user)
        resp = api_client.get(reverse("labtest-list"))
        assert resp.status_code == status.HTTP_403_FORBIDDEN