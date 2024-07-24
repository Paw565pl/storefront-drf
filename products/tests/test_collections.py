import pytest
from rest_framework import status

from products.models import Collection


@pytest.mark.django_db
class TestListCollection:
    def test_if_no_collections_exist_returns_200(self, api_client):
        response = api_client.get(
            "/api/collections/", headers={"Cache-Control": "no-store"}
        )
        results = response.data.get("results")
        print(results)

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_collections_exist_returns_200(self, create_collection, api_client):
        response = api_client.get(
            "/api/collections/", headers={"Cache-Control": "no-store"}
        )
        results = response.data.get("results")
        print(results)
        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/collections/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_collection_by_id_returns_200(self, api_client, create_collection):
        collection_id = create_collection.id
        response = api_client.get(f"/api/collections/{collection_id}/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/api/collections/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/collections/", {})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, admin_api_client):
        payload = {"title": ""}
        response = admin_api_client.post("/api/collections/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, admin_api_client):
        payload = {"title": "test"}

        response = admin_api_client.post("/api/collections/", payload)
        result = response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert result["title"] == payload["title"]


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection, api_client):
        collection_id = create_collection.id
        response = api_client.put(f"/api/collections/{collection_id}/", {})

        assert response.status_code == 401

    def test_if_user_is_not_admin_returns_403(
        self, create_collection, authenticated_api_client
    ):
        collection_id = create_collection.id
        response = authenticated_api_client.put(
            f"/api/collections/{collection_id}/", {}
        )

        assert response.status_code == 403

    def test_if_data_is_invalid_returns_400(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        payload = {"title": ""}

        response = admin_api_client.put(f"/api/collections/{collection_id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        payload = {"title": "test"}

        response = admin_api_client.put(f"/api/collections/{collection_id}/", payload)
        result = response.data

        assert response.status_code == status.HTTP_200_OK
        assert result["title"] == payload["title"]


@pytest.mark.django_db
class TestPartialUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection, api_client):
        collection_id = create_collection.id
        response = api_client.patch(f"/api/collections/{collection_id}/", {})

        assert response.status_code == 401

    def test_if_user_is_not_admin_returns_403(
        self, create_collection, authenticated_api_client
    ):
        collection_id = create_collection.id
        response = authenticated_api_client.patch(
            f"/api/collections/{collection_id}/", {}
        )

        assert response.status_code == 403

    def test_if_data_is_invalid_returns_400(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        payload = {"title": ""}

        response = admin_api_client.patch(f"/api/collections/{collection_id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        payload = {"title": "test"}

        response = admin_api_client.patch(f"/api/collections/{collection_id}/", payload)
        result = response.data

        assert response.status_code == status.HTTP_200_OK
        assert result["title"] == payload["title"]


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_anonymous_returns_401(self, create_collection, api_client):
        collection_id = create_collection.id
        response = api_client.delete(f"/api/collections/{collection_id}/")

        assert response.status_code == 401

    def test_if_user_is_not_admin_returns_403(
        self, create_collection, authenticated_api_client
    ):
        collection_id = create_collection.id
        response = authenticated_api_client.delete(f"/api/collections/{collection_id}/")

        assert response.status_code == 403

    def test_if_collection_has_products_returns_409(
        self, create_product, admin_api_client
    ):
        collection_id = create_product.collection.id
        response = admin_api_client.delete(f"/api/collections/{collection_id}/")

        assert response.status_code == 409

    def test_if_user_is_admin_returns_204(self, create_collection, admin_api_client):
        collection_id = create_collection.id
        response = admin_api_client.delete(f"/api/collections/{collection_id}/")

        assert response.status_code == 204
        assert not Collection.objects.filter(id=collection_id).exists()
