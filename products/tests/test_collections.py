import pytest

from products.models import Collection


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
