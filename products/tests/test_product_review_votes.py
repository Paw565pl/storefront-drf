import pytest
from rest_framework import status

from products.models import Review


@pytest.mark.django_db
class TestCreateProductReviewVote:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_review_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/products/1/reviews/1/vote/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_vote_already_exists_returns_409(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        payload = {"value": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_data_is_valid_returns_201(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        payload = {"value": 1}

        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["value"] == payload["value"]
        assert Review.objects.get(id=product_review.id).votes.filter(**payload).exists()


@pytest.mark.django_db
class TestRetrieveProductReviewVote:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.get(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_review_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.get("/api/products/1/reviews/1/vote/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vote_does_not_exist_returns_404(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.get(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vote_exists_returns_200(self, authenticated_api_client, product_review):
        product_id = product_review.product.id
        payload = {"value": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        response = authenticated_api_client.get(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["value"] == payload["value"]


@pytest.mark.django_db
class TestUpdateProductReviewVote:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_review_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.put("/api/products/1/reviews/1/vote/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vote_does_not_exist_returns_404(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        payload = {"value": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        payload = {"value": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        update_payload = {"value": -1}
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/",
            update_payload,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["value"] == update_payload["value"]
        assert (
            Review.objects.get(id=product_review.id)
            .votes.filter(**update_payload)
            .exists()
        )


@pytest.mark.django_db
class TestDeleteProductReviewVote:
    def test_if_user_is_anonymous_returns_401(self, api_client, product_review):
        product_id = product_review.product.id
        response = api_client.delete(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_review_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.delete("/api/products/1/reviews/1/vote/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vote_does_not_exist_returns_404(
        self, authenticated_api_client, product_review
    ):
        product_id = product_review.product.id
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_vote_exists_returns_204(self, authenticated_api_client, product_review):
        product_id = product_review.product.id
        payload = {"value": 1}
        authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/", payload
        )

        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{product_review.id}/vote/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (
            not Review.objects.get(id=product_review.id)
            .votes.filter(**payload)
            .exists()
        )
