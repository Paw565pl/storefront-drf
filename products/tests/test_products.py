import pytest
from rest_framework import status

from products.serializers import ProductSerializer


@pytest.mark.django_db
def test_retrieve_product_by_id_and_slug_returns_200(client, create_product):
    product_id = create_product.id
    product_slug = create_product.slug

    serialized_product = ProductSerializer(create_product)

    id_response = client.get(f"/api/products/{product_id}/")
    slug_response = client.get(f"/api/products/{product_slug}/")

    assert id_response.status_code == status.HTTP_200_OK
    assert slug_response.status_code == status.HTTP_200_OK

    assert id_response.data == serialized_product.data
    assert slug_response.data == serialized_product.data
    assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, client):
        response = client.post("/api/products/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/products/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, admin_api_client):
        test_product = {"title": "test", "unit_price": "10.00", "collection_id": 1}
        response = admin_api_client.post("/api/products/", test_product)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        test_product = {
            "title": "test",
            "unit_price": "10.00",
            "collection_id": collection_id,
        }
        response = admin_api_client.post("/api/products/", test_product)

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, client):
        response = client.put("/api/products/1/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.put("/api/products/1/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_product, admin_api_client):
        product_id = create_product.id
        test_product = {"title": "test", "unit_price": "10.00", "collection_id": 1}
        response = admin_api_client.put(f"/api/products/{product_id}/", test_product)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, create_product, create_collection, admin_api_client
    ):
        product_id = create_product.id
        collection_id = create_collection.id
        test_product = {
            "title": "test",
            "unit_price": "20.00",
            "collection_id": collection_id,
        }
        response = admin_api_client.put(f"/api/products/{product_id}/", test_product)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == test_product["title"]
        assert response.data["unit_price"] == test_product["unit_price"]
        assert response.data["collection"]["id"] == test_product["collection_id"]
