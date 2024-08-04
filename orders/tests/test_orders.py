from uuid import uuid4

import pytest
from rest_framework import status

from orders.models import Order
from orders.serializers import OrderSerializer

URL = "/api/orders/"


@pytest.mark.django_db
class TestListOrders:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_no_orders_returns_200(self, authenticated_api_client):
        response = authenticated_api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_user_has_orders_returns_200(self, api_client, test_user, create_order):
        order = create_order(test_user.customer)
        serialized_order = OrderSerializer(order).data
        api_client.force_authenticate(user=test_user)

        response = api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0] == serialized_order

    def test_if_user_is_admin_returns_200(
        self, admin_api_client, test_user, create_order
    ):
        order = create_order(test_user.customer)
        serialized_order = OrderSerializer(order).data

        response = admin_api_client.get(URL)
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0] == serialized_order


@pytest.mark.django_db
class TestCreateOrder:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, authenticated_api_client):
        response = authenticated_api_client.post(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_cart_does_not_exist_returns_400(self, authenticated_api_client):
        payload = {"cart_id": uuid4()}
        response = authenticated_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_cart_is_empty_returns_400(self, authenticated_api_client, cart):
        payload = {"cart_id": cart.id}
        response = authenticated_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_has_no_address_returns_400(
        self, authenticated_api_client, cart, create_cart_item
    ):
        create_cart_item(cart)

        payload = {"cart_id": cart.id}
        response = authenticated_api_client.post(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(
        self, api_client, test_user, create_customer_address, cart, create_cart_item
    ):
        create_cart_item(cart)
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        payload = {"cart_id": cart.id}
        response = api_client.post(URL, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1


@pytest.mark.django_db
class TestRetrieveOrder:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get(URL + "1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_order_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.get(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_order_exists_returns_200(self, api_client, test_user, create_order):
        order = create_order(test_user.customer)
        serialized_order = OrderSerializer(order).data
        api_client.force_authenticate(user=test_user)

        response = api_client.get(URL + f"{order.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_order


@pytest.mark.django_db
class TestPartialUpdateOrder:
    def test_if_user_is_anonymous_returns_404(self, api_client):
        response = api_client.patch(URL + "1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.patch(URL + "1/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_order_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.patch(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, admin_api_client, test_user, create_order
    ):
        order = create_order(test_user.customer)

        response = admin_api_client.patch(URL + f"{order.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, admin_api_client, test_user, create_order
    ):
        order = create_order(test_user.customer)

        payload = {"status": "D"}
        response = admin_api_client.patch(URL + f"{order.id}/", payload)

        assert response.status_code == status.HTTP_200_OK
        assert Order.objects.get(id=order.id).status == payload["status"]


@pytest.mark.django_db
class TestDeleteOrder:
    def test_if_user_is_anonymous_returns_404(self, api_client):
        response = api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticated_api_client):
        response = authenticated_api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_order_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.delete(URL + "1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_valid_returns_204(
        self, admin_api_client, test_user, create_order
    ):
        order = create_order(test_user.customer)

        response = admin_api_client.delete(URL + f"{order.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(id=order.id).exists()
