import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from passwords.models import Password


@pytest.mark.django_db
class TestPasswordView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    @pytest.fixture
    def create_password(self):
        return Password.objects.create(service_name="yandex", password="secret_pass")

    def test_create_password(self):
        url = reverse("password-create-retrieve", kwargs={"service_name": "yandex"})
        response = self.client.post(url, {"password": "secret_pass"})
        assert response.status_code == status.HTTP_201_CREATED
        assert Password.objects.count() == 1
        assert Password.objects.get().service_name == "yandex"

    def test_update_password(self, create_password):
        url = reverse("password-create-retrieve", kwargs={"service_name": "yandex"})
        response = self.client.post(url, {"password": "new_pass"})
        assert response.status_code == status.HTTP_200_OK
        assert Password.objects.count() == 1

        updated_password = Password.objects.get(service_name="yandex")
        assert updated_password.get_decrypted_password() == "new_pass"

    def test_get_password_by_service_name(self, create_password):
        url = reverse("password-create-retrieve", kwargs={"service_name": "yandex"})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["password"] == "secret_pass"
        assert response.data[0]["service_name"] == "yandex"

    def test_get_password_by_partial_service_name(self, create_password):
        url = reverse("password-search") + "?service_name=yan"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["service_name"] == "yandex"

    def test_no_matching_services(self):
        url = reverse("password-search") + "?service_name=nonexistent"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No matching services found."

    def test_create_password_without_password_field(self):
        url = reverse("password-create-retrieve", kwargs={"service_name": "yandex"})
        response = self.client.post(url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Password is required."
