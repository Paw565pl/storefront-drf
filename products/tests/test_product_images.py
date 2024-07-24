import pytest
from rest_framework import status


@pytest.mark.django_db
class TestListProductImages:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/images/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_exists_returns_200(self, api_client, create_product_image):
        product_id = create_product_image.product.id
        product_slug = create_product_image.product.slug

        id_response = api_client.get(f"/api/products/{product_id}/images/")
        slug_response = api_client.get(f"/api/products/{product_slug}/images/")

        assert id_response.status_code == status.HTTP_200_OK
        assert slug_response.status_code == status.HTTP_200_OK

        assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestCreateProductImage:
    def test_if_product_does_not_exist_returns_404(self, admin_api_client):
        response = admin_api_client.post("/api/products/1/images/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_valid_returns_201(
        self, admin_api_client, create_product, create_image_file
    ):
        file = create_image_file()

        product_id = create_product.id
        test_image = {"image": file}

        response = admin_api_client.post(
            f"/api/products/{product_id}/images/", test_image
        )

        assert response.status_code == status.HTTP_201_CREATED
