import pytest
from rest_framework import status

from orders.models import CustomerAddress
from orders.serializers import CustomerAddressSerializer

URL = "/api/address/"
VALID_DATA = {
    "first_name": "test",
    "last_name": "test",
    "phone_number": "+41" + "5" * 9,
    "apartment_number": "test",
    "street_number": "test",
    "street": "test",
    "postal_code": "test",
    "city": "test",
    "state": "test",
    "country": "test",
}


@pytest.mark.django_db
class TestRetrieveCustomerAddress:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_address_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.get(URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_address_exists_returns_200(
        self, api_client, test_user, create_customer_address
    ):
        customer_address = create_customer_address(test_user.customer)
        serialized_customer_address = CustomerAddressSerializer(customer_address).data
        api_client.force_authenticate(user=test_user)

        response = api_client.get(URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_customer_address


@pytest.mark.django_db
class TestCreateCustomerAddress:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_returns_400(self, authenticated_api_client):
        response = authenticated_api_client.post(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, authenticated_api_client):
        response = authenticated_api_client.post(URL, VALID_DATA)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["first_name"] == VALID_DATA["first_name"]
        assert response.data["last_name"] == VALID_DATA["last_name"]

    def test_if_address_already_exists_returns(
        self, api_client, test_user, create_customer_address
    ):
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        response = api_client.post(URL, VALID_DATA)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUpdateCustomerAddress:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_address_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.put(URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, api_client, test_user, create_customer_address
    ):
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        response = api_client.put(URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, api_client, test_user, create_customer_address
    ):
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        payload = VALID_DATA.copy()
        payload["first_name"] = "updated"
        response = api_client.put(URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == payload["first_name"]


@pytest.mark.django_db
class TestPartialUpdateCustomerAddress:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.patch(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_address_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.patch(URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, api_client, test_user, create_customer_address
    ):
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        payload = {"first_name": ""}
        response = api_client.patch(URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, api_client, test_user, create_customer_address
    ):
        create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        payload = {"first_name": "updated"}
        response = api_client.patch(URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == payload["first_name"]


@pytest.mark.django_db
class TestDeleteCustomerAddress:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete(URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_address_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.delete(URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_delete_returns_204(
        self, api_client, test_user, create_customer_address
    ):
        customer_address = create_customer_address(test_user.customer)
        api_client.force_authenticate(user=test_user)

        response = api_client.delete(URL)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CustomerAddress.objects.filter(id=customer_address.id).exists()
