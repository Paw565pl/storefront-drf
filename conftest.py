import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, django_user_model):
    user = baker.make(django_user_model)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(api_client, django_user_model):
    user = baker.make(django_user_model, is_staff=True)
    api_client.force_authenticate(user=user)
    return api_client
