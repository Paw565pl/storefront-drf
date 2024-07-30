from uuid import uuid4

import pytest
from rest_framework import status

from orders.models import CartItem
from orders.serializers import CartItemSerializer


@pytest.mark.django_db
class TestListCartItems:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.get(f"/api/carts/{uuid4()}/items/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_item_does_not_exist_returns_200(self, api_client, cart):
        response = api_client.get(f"/api/carts/{cart.id}/items/")
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_item_exists_returns_200(self, api_client, cart, create_cart_item):
        cart_item = create_cart_item(cart, 1)
        serialized_cart_item = CartItemSerializer(cart_item).data

        response = api_client.get(f"/api/carts/{cart.id}/items/")
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0] == serialized_cart_item


@pytest.mark.django_db
class TestCreateCartItem:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.post(f"/api/carts/{uuid4()}/items/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, api_client, cart):
        payload = {"product_id": 0}
        response = api_client.post(f"/api/carts/{cart.id}/items/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_quantity_is_too_big_returns_400(self, api_client, product, cart):
        payload = {"product_id": product.id, "quantity": product.inventory + 1}
        response = api_client.post(f"/api/carts/{cart.id}/items/", payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, api_client, product, cart):
        payload = {"product_id": product.id, "quantity": 1}
        response = api_client.post(f"/api/carts/{cart.id}/items/", payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["product"]["id"] == payload["product_id"]
        assert response.data["quantity"] == payload["quantity"]
        assert CartItem.objects.filter(cart=cart, **payload).exists()

    def test_if_item_already_exists_returns_201(self, api_client, product, cart):
        expected_quantity = 2
        payload = {"product_id": product.id, "quantity": 1}
        api_client.post(f"/api/carts/{cart.id}/items/", payload)

        response = api_client.post(f"/api/carts/{cart.id}/items/", payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["product"]["id"] == payload["product_id"]
        assert response.data["quantity"] == expected_quantity
        assert CartItem.objects.filter(
            cart=cart,
            id=response.data["id"],
            product_id=product.id,
            quantity=expected_quantity,
        ).exists()


@pytest.mark.django_db
class TestRetrieveCartItem:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.get(f"/api/carts/{uuid4()}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_item_does_not_exist_returns_404(self, api_client, cart):
        response = api_client.get(f"/api/carts/{cart.id}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_item_exists_returns_200(self, api_client, cart, create_cart_item):
        cart_item = create_cart_item(cart, 1)
        serialized_cart_item = CartItemSerializer(cart_item).data

        response = api_client.get(f"/api/carts/{cart.id}/items/{cart_item.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_cart_item


@pytest.mark.django_db
class TestPartialUpdateCartItem:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.patch(f"/api/carts/{uuid4()}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_item_does_not_exist_returns_404(self, api_client, cart):
        response = api_client.patch(f"/api/carts/{cart.id}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, api_client, cart, create_cart_item):
        cart_item = create_cart_item(cart, 1)
        response = api_client.patch(f"/api/carts/{cart.id}/items/{cart_item.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_quantity_is_too_big_returns_400(
        self, api_client, product, cart, create_cart_item
    ):
        cart_item = create_cart_item(cart, 1)

        payload = {"quantity": product.inventory + 1}
        response = api_client.patch(
            f"/api/carts/{cart.id}/items/{cart_item.id}/", payload
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, api_client, product, cart, create_cart_item
    ):
        cart_item = create_cart_item(cart, 1)
        cart_item.product = product
        cart_item.save()

        expected_quantity = 3
        payload = {"quantity": expected_quantity}
        response = api_client.patch(
            f"/api/carts/{cart.id}/items/{cart_item.id}/", payload
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["quantity"] == expected_quantity
        assert CartItem.objects.filter(
            cart=cart, id=cart_item.id, quantity=expected_quantity
        ).exists()


@pytest.mark.django_db
class TestDeleteCartItem:
    def test_if_cart_does_not_exist_returns_404(self, api_client):
        response = api_client.delete(f"/api/carts/{uuid4()}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_item_does_not_exist_returns_404(self, api_client, cart):
        response = api_client.delete(f"/api/carts/{cart.id}/items/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_delete_returns_204(self, api_client, cart, create_cart_item):
        cart_item = create_cart_item(cart, 1)
        response = api_client.delete(f"/api/carts/{cart.id}/items/{cart_item.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CartItem.objects.filter(cart=cart, id=cart_item.id).exists()
