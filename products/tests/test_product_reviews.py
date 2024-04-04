import pytest
from rest_framework import status


@pytest.mark.django_db
class TestListProductReviews:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/reviews/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_exists_returns_200(self, create_product_review, api_client):
        product_id = create_product_review.product.id
        product_slug = create_product_review.product.slug

        id_response = api_client.get(f"/api/products/{product_id}/reviews/")
        slug_response = api_client.get(f"/api/products/{product_slug}/reviews/")

        assert id_response.status_code == status.HTTP_200_OK
        assert slug_response.status_code == status.HTTP_200_OK

        assert id_response.data == slug_response.data


@pytest.mark.django_db
class TestCreateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/api/products/1/reviews/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_already_has_review_returns_409(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_review = {"content": "test test test", "rating": 5}

        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", test_review
        )
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", test_review
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_data_is_valid_returns_201(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_review = {"content": "test test test", "rating": 5}

        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", test_review
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == test_review["content"]
        assert response.data["rating"] == test_review["rating"]


@pytest.mark.django_db
class TestUpdateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.put("/api/products/1/reviews/1/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_review_does_not_exist_returns_404(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/1/", {}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_not_author_returns_403(
        self, create_product, create_product_review, authenticated_api_client
    ):
        product_id = create_product.id
        review_id = create_product_review.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_200(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_review = {"content": "test test test", "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", test_review
        )

        review_id = create_response.data["id"]
        test_update_review = {"content": "test 123 test test", "rating": 1}
        update_response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", test_update_review
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["content"] == test_update_review["content"]
        assert update_response.data["rating"] == test_update_review["rating"]


@pytest.mark.django_db
class TestDeleteProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, create_product, create_product_review, authenticated_api_client
    ):
        product_id = create_product.id
        review_id = create_product_review.id
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{review_id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_204(
        self, create_product, authenticated_api_client
    ):
        product_id = create_product.id
        test_review = {"content": "test test test", "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", test_review
        )

        review_id = create_response.data["id"]
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{review_id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
