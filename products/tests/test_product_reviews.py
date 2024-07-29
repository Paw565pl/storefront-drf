import pytest
from rest_framework import status

from products.models import Review

VALID_DATA = {"content": "a" * 10, "rating": 5}


@pytest.mark.django_db
class TestListProductReviews:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/reviews/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_200(self, api_client, product):
        response = api_client.get(f"/api/products/{product.id}/reviews/")
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 0

    def test_if_review_exists_returns_200(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.get(f"/api/products/{product_id}/reviews/")
        results = response.data["results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["rating"] == product_review.rating
        assert results[0]["content"] == product_review.content


@pytest.mark.django_db
class TestCreateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/api/products/1/reviews/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/products/1/reviews/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, authenticated_api_client, product):
        response = authenticated_api_client.post(f"/api/products/{product.id}/reviews/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_already_has_review_for_product_returns_409(
        self, authenticated_api_client, product
    ):
        authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_data_is_valid_returns_201(self, authenticated_api_client, product):
        response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == VALID_DATA["content"]
        assert response.data["rating"] == VALID_DATA["rating"]
        assert Review.objects.filter(**VALID_DATA).exists()


@pytest.mark.django_db
class TestRetrieveProductReview:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(self, api_client, product):
        response = api_client.get(f"/api/products/{product.id}/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_exists_returns_200(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.get(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product_review.id
        assert response.data["rating"] == product_review.rating
        assert response.data["content"] == product_review.content


@pytest.mark.django_db
class TestUpdateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.put("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, product
    ):
        response = authenticated_api_client.put(
            f"/api/products/{product.id}/reviews/1/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, authenticated_api_client, product):
        create_response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        review_id = create_response.data["id"]
        update_response = authenticated_api_client.put(
            f"/api/products/{product.id}/reviews/{review_id}/"
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, authenticated_api_client, product):
        create_response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        review_id = create_response.data["id"]
        payload = {"content": "b" * 10, "rating": 10}
        update_response = authenticated_api_client.put(
            f"/api/products/{product.id}/reviews/{review_id}/", payload
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["content"] == payload["content"]
        assert update_response.data["rating"] == payload["rating"]
        assert Review.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestPartialUpdateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.patch(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.patch(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.patch("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, product
    ):
        response = authenticated_api_client.patch(
            f"/api/products/{product.id}/reviews/1/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(self, authenticated_api_client, product):
        create_response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        review_id = create_response.data["id"]
        payload = {"rating": 0}
        update_response = authenticated_api_client.patch(
            f"/api/products/{product.id}/reviews/{review_id}/", payload
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, authenticated_api_client, product):
        create_response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        review_id = create_response.data["id"]
        payload = {"rating": 1}
        update_response = authenticated_api_client.patch(
            f"/api/products/{product.id}/reviews/{review_id}/", payload
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["content"] == VALID_DATA["content"]
        assert update_response.data["rating"] == payload["rating"]
        assert Review.objects.filter(**payload).exists()


@pytest.mark.django_db
class TestDeleteProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.delete(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{product_review.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.delete("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, product
    ):
        response = authenticated_api_client.delete(
            f"/api/products/{product.id}/reviews/1/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_author_returns_204(
        self,
        authenticated_api_client,
        product,
    ):
        create_response = authenticated_api_client.post(
            f"/api/products/{product.id}/reviews/", VALID_DATA
        )

        review_id = create_response.data["id"]
        delete_response = authenticated_api_client.delete(
            f"/api/products/{product.id}/reviews/{review_id}/"
        )

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(id=review_id).exists()
