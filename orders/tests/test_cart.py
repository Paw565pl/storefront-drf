import pytest
from rest_framework import status

from orders.models import Cart

URL = "/api/carts/"


@pytest.mark.django_db
class TestCreateCart:
    def test_if_create_cart_returns_201(self, api_client):
        response = api_client.post(URL)

        assert response.status_code == status.HTTP_201_CREATED
        assert Cart.objects.filter(id=response.data["id"]).exists()


@pytest.mark.django_db
class TestRetrieveCart:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.get(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_cart_exists_returns_200(self, api_client, cart):
        cart_id = cart.id.__str__()
        response = api_client.get(URL + f"{cart_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == cart_id


@pytest.mark.django_db
class TestDeleteCart:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_delete_returns_204(self, api_client, cart):
        cart_id = cart.id.__str__()
        response = api_client.delete(URL + f"{cart_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
