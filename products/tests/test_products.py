import pytest
from rest_framework import status

from products.models import Product

URL = "/api/products/"


@pytest.mark.django_db
class TestListProducts:
    def test_if_product_does_not_exist_returns_200(self, api_client):
        response = api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_product_exist_returns_200(self, api_client, product):
        response = api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["title"] == product.title


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.post(URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, admin_api_client):
        response = admin_api_client.post(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_does_not_exist_returns_400(self, admin_api_client):
        payload = {
            "title": "test",
            "unit_price": "10.00",
            "collection_id": 0,
        }
        response = admin_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, admin_api_client, collection):
        payload = {
            "title": "test",
            "unit_price": "10.00",
            "collection_id": collection.id,
        }
        response = admin_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == payload["title"]
        assert response.data["unit_price"] == payload["unit_price"]
        assert response.data["collection"]["id"] == payload["collection_id"]
        assert Product.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_product_by_id_or_slug_returns_200(self, api_client, product):
        id_response = api_client.get(URL + f"{product.id}/")
        slug_response = api_client.get(URL + f"{product.slug}/")

        assert id_response.status_code == status.HTTP_200_OK
        assert slug_response.status_code == status.HTTP_200_OK
        assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, product):
        response = api_client.put(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client, product):
        response = authenticated_api_client.put(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.put(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, admin_api_client, product):
        response = admin_api_client.put(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_does_not_exist_returns_400(self, admin_api_client, product):
        payload = {
            "title": "test",
            "unit_price": "10.00",
            "collection_id": 0,
        }
        response = admin_api_client.put(URL + f"{product.id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, product, collection, admin_api_client):
        payload = {
            "title": "test",
            "unit_price": "20.00",
            "collection_id": collection.id,
        }
        response = admin_api_client.put(URL + f"{product.id}/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == payload["title"]
        assert response.data["unit_price"] == payload["unit_price"]
        assert response.data["collection"]["id"] == payload["collection_id"]
        assert Product.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestPartialUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, product):
        response = api_client.patch(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client, product):
        response = authenticated_api_client.patch(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.patch(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, admin_api_client, product):
        payload = {"unit_price": "abc"}
        response = admin_api_client.patch(URL + f"{product.id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_does_not_exist_returns_400(self, admin_api_client, product):
        payload = {
            "collection_id": 0,
        }
        response = admin_api_client.patch(URL + f"{product.id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, admin_api_client, product, collection):
        payload = {
            "title": "test",
        }
        response = admin_api_client.patch(URL + f"{product.id}/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == payload["title"]
        assert Product.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, product):
        response = api_client.delete(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client, product):
        response = authenticated_api_client.delete(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_204(self, product, admin_api_client):
        response = admin_api_client.delete(URL + f"{product.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product.id).exists()
