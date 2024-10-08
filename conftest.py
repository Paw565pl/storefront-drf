import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework.test import APIClient

from products.models import Product, Collection


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, django_user_model) -> APIClient:
    user = baker.make(django_user_model)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(api_client, django_user_model) -> APIClient:
    user = baker.make(django_user_model, is_staff=True)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def test_user(django_user_model):
    user = baker.make(django_user_model)
    return user


@pytest.fixture
def create_image_file():
    def do_create_image_file() -> SimpleUploadedFile:
        file = SimpleUploadedFile(
            "test_image.jpeg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b",
            "image/jpeg",
        )
        return file

    return do_create_image_file


@pytest.fixture
def collection() -> Collection:
    collection = baker.make(Collection)
    return collection


@pytest.fixture
def product(collection) -> Product:
    product = baker.make(Product, collection=collection, inventory=10)
    return product
