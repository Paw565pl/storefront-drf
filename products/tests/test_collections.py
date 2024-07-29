import pytest
from rest_framework import status

from products.models import Collection
from products.serializers import CollectionSerializer

URL = "/api/collections/"


@pytest.mark.django_db
class TestListCollection:
    def test_if_collection_does_not_exist_returns_200(self, api_client):
        response = api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_collection_exist_returns_200(self, api_client, collection):
        serialized_collection = CollectionSerializer(collection).data

        response = api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0] == serialized_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.post(URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, admin_api_client):
        response = admin_api_client.post(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_collection_already_exists_returns_400(
        self, admin_api_client, collection
    ):
        payload = {"title": collection.title}
        response = admin_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, admin_api_client):
        payload = {"title": "test"}
        response = admin_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == payload["title"]
        assert Collection.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_does_not_exist_returns_404(self, api_client):
        response = api_client.get(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_collection_by_id_returns_200(self, api_client, collection):
        serialized_collection = CollectionSerializer(collection).data

        response = api_client.get(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_collection


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client, collection):
        response = api_client.put(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, collection
    ):
        response = authenticated_api_client.put(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.put(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, admin_api_client, collection):
        response = admin_api_client.put(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, admin_api_client, collection):
        payload = {"title": "test"}
        response = admin_api_client.put(URL + f"{collection.id}/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == payload["title"]
        assert Collection.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestPartialUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client, collection):
        response = api_client.patch(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, collection
    ):
        response = authenticated_api_client.patch(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.patch(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, admin_api_client, collection):
        payload = {"title": ""}
        response = admin_api_client.patch(URL + f"{collection.id}/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, admin_api_client, collection):
        payload = {"title": "test"}
        response = admin_api_client.patch(URL + f"{collection.id}/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == payload["title"]
        assert Collection.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client, collection):
        response = api_client.delete(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, collection
    ):
        response = authenticated_api_client.delete(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_has_products_returns_409(self, admin_api_client, product):
        collection_id = product.collection.id
        response = admin_api_client.delete(URL + f"{collection_id}/")

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_user_is_admin_returns_204(self, admin_api_client, collection):
        response = admin_api_client.delete(URL + f"{collection.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Collection.objects.filter(id=collection.id).exists()
