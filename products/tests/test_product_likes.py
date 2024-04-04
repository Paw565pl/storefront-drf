import pytest
from rest_framework import status


@pytest.mark.django_db
class TestRetrieveProductLikesDislikes:
    def test_if_user_is_anonymous_returns_401(self, create_product, api_client):
        product_id = create_product.id

        response = api_client.get(f"/api/products/{product_id}/like_dislike/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.get("/api/products/1/like_dislike/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_has_no_like_dislike_returns_404(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        product_slug = create_product.slug

        response = authenticated_api_client.get(
            f"/api/products/{product_id}/like_dislike/"
        )
        response_slug = authenticated_api_client.get(
            f"/api/products/{product_slug}/like_dislike/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_slug.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_has_like_dislike_returns_200(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        product_slug = create_product.slug

        test_like_dislike = {"vote": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )

        id_response = authenticated_api_client.get(
            f"/api/products/{product_id}/like_dislike/"
        )
        slug_response = authenticated_api_client.get(
            f"/api/products/{product_slug}/like_dislike/"
        )

        assert id_response.status_code == status.HTTP_200_OK
        assert slug_response.status_code == status.HTTP_200_OK

        assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestCreateProductLikeDislike:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(f"/api/products/1/like_dislike/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_already_has_like_dislike_returns_409(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_like_dislike = {"vote": 1}

        authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_data_is_valid_returns_201(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_like_dislike = {"vote": 1}

        response = authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["vote"] == test_like_dislike["vote"]


@pytest.mark.django_db
class TestUpdateProductLikeDislike:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put(f"/api/products/1/like_dislike/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_like_dislike_does_not_exist_returns_404(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/like_dislike/", {}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_valid_returns_200(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_like_dislike = {"vote": 1}
        updated_like_dislike = {"vote": -1}

        authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/like_dislike/", updated_like_dislike
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["vote"] == updated_like_dislike["vote"]


@pytest.mark.django_db
class TestDeleteProductLikeDislike:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete(f"/api/products/1/like_dislike/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_like_dislike_does_not_exist_returns_404(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/like_dislike/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_has_like_dislike_returns_204(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_like_dislike = {"vote": 1}

        authenticated_api_client.post(
            f"/api/products/{product_id}/like_dislike/", test_like_dislike
        )
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/like_dislike/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
