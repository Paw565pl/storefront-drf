import pytest
from rest_framework import status


@pytest.mark.django_db
class TestListProducts:
    def test_if_no_products_exist_returns_200(self, api_client):
        response = api_client.get("/api/products/")
        results = response.data.get("results")

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_products_exist_returns_200(self, create_product, api_client):
        response = api_client.get("/api/products/")
        results = response.data.get("results")

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1


@pytest.mark.django_db
class TestRetrieveProducts:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_product_by_id_or_slug_returns_200(
        self, api_client, create_product
    ):
        product_id = create_product.id
        product_slug = create_product.slug

        id_response = api_client.get(f"/api/products/{product_id}/")
        slug_response = api_client.get(f"/api/products/{product_slug}/")

        assert id_response.status_code == status.HTTP_200_OK
        assert slug_response.status_code == status.HTTP_200_OK

        assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/api/products/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/products/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, admin_api_client):
        payload = {"title": "test", "unit_price": "abc", "collection_id": 1}
        response = admin_api_client.post("/api/products/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        payload = {
            "title": "test",
            "unit_price": "10.00",
            "collection_id": collection_id,
        }

        response = admin_api_client.post("/api/products/", payload)
        result = response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert result["title"] == payload["title"]
        assert result["unit_price"] == payload["unit_price"]
        assert result["collection"]["id"] == payload["collection_id"]


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put("/api/products/1/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.put("/api/products/1/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_product, admin_api_client):
        product_id = create_product.id
        payload = {"title": "test", "unit_price": "abc", "collection_id": 1}

        response = admin_api_client.put(f"/api/products/{product_id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, create_product, create_collection, admin_api_client
    ):
        product_id = create_product.id
        collection_id = create_collection.id
        payload = {
            "title": "test",
            "unit_price": "20.00",
            "collection_id": collection_id,
        }

        response = admin_api_client.put(f"/api/products/{product_id}/", payload)
        result = response.data

        assert response.status_code == status.HTTP_200_OK
        assert result["title"] == payload["title"]
        assert result["unit_price"] == payload["unit_price"]
        assert result["collection"]["id"] == payload["collection_id"]


@pytest.mark.django_db
class TestPartialUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.patch("/api/products/1/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.patch("/api/products/1/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_product, admin_api_client):
        product_id = create_product.id
        payload = {"unit_price": "abc"}

        response = admin_api_client.patch(f"/api/products/{product_id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, create_product, create_collection, admin_api_client
    ):
        product_id = create_product.id
        payload = {
            "title": "test",
        }

        response = admin_api_client.patch(f"/api/products/{product_id}/", payload)
        result = response.data

        assert response.status_code == status.HTTP_200_OK
        assert result["title"] == payload["title"]


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete("/api/products/1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.delete("/api/products/1/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_204(self, create_product, admin_api_client):
        product_id = create_product.id
        response = admin_api_client.delete(f"/api/products/{product_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
