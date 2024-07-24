import pytest
from rest_framework import status

from products.models import ProductImage


@pytest.mark.django_db
class TestListProductImages:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/images/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_exists_returns_200(self, api_client, create_product_image):
        product_id = create_product_image.product.id

        response = api_client.get(f"/api/products/{product_id}/images/")
        results = response.data.get("results")

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1


@pytest.mark.django_db
class TestCreateProductImage:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
        product_id = create_product.id
        response = api_client.post(f"/api/products/{product_id}/images/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/images/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.post("/api/products/1/images/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, admin_api_client, create_product):
        product_id = create_product.id
        response = admin_api_client.post(f"/api/products/{product_id}/images/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(
        self, admin_api_client, create_product, create_image_file
    ):
        product_id = create_product.id

        file = create_image_file()
        payload = {"image": file}

        response = admin_api_client.post(f"/api/products/{product_id}/images/", payload)

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveProductImage:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/images/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_image_does_not_exist_returns_404(self, api_client, create_product):
        product_id = create_product.id
        response = api_client.get(f"/api/products/{product_id}/images/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_image_exists_returns_200(self, api_client, create_product_image):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = api_client.get(f"/api/products/{product_id}/images/{image_id}/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateProductImage:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_image):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = api_client.put(f"/api/products/{product_id}/images/{image_id}/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, create_product_image
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = authenticated_api_client.put(
            f"/api/products/{product_id}/images/{image_id}/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.put("/api/products/1/images/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_image_does_not_exist_returns_404(
        self, admin_api_client, create_product
    ):
        product_id = create_product.id
        response = admin_api_client.put(f"/api/products/{product_id}/images/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, admin_api_client, create_product_image
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = admin_api_client.put(
            f"/api/products/{product_id}/images/{image_id}/", {}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, admin_api_client, create_product_image, create_image_file
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        file = create_image_file()
        payload = {"image": file}

        response = admin_api_client.put(
            f"/api/products/{product_id}/images/{image_id}/", payload
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPartialUpdateProductImage:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_image):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = api_client.patch(
            f"/api/products/{product_id}/images/{image_id}/", {}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, create_product_image
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = authenticated_api_client.patch(
            f"/api/products/{product_id}/images/{image_id}/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.patch("/api/products/1/images/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_image_does_not_exist_returns_404(
        self, admin_api_client, create_product
    ):
        product_id = create_product.id
        response = admin_api_client.patch(f"/api/products/{product_id}/images/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, admin_api_client, create_product_image
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        payload = {"image": "a"}
        response = admin_api_client.patch(
            f"/api/products/{product_id}/images/{image_id}/", payload
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, admin_api_client, create_product_image, create_image_file
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        file = create_image_file()
        payload = {"image": file}

        response = admin_api_client.patch(
            f"/api/products/{product_id}/images/{image_id}/", payload
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteProductImage:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_image):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = api_client.delete(f"/api/products/{product_id}/images/{image_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, authenticated_api_client, create_product_image
    ):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/images/{image_id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.delete("/api/products/1/images/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_image_does_not_exist_returns_404(
        self, admin_api_client, create_product
    ):
        product_id = create_product.id
        response = admin_api_client.delete(f"/api/products/{product_id}/images/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_admin_returns_204(self, admin_api_client, create_product_image):
        product_id = create_product_image.product.id
        image_id = create_product_image.id

        response = admin_api_client.delete(
            f"/api/products/{product_id}/images/{image_id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProductImage.objects.filter(id=image_id).exists()
