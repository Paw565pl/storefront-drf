import pytest
from rest_framework import status

from products.models import Review


@pytest.mark.django_db
class TestListProductReviews:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/reviews/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_exists_returns_200(self, api_client, create_product_review):
        product_id = create_product_review.product.id

        response = api_client.get(f"/api/products/{product_id}/reviews/")
        results = response.data.get("results")

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1


@pytest.mark.django_db
class TestCreateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post("/api/products/1/reviews/", {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.post("/api/products/1/reviews/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", {}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_already_has_review_for_product_returns_409(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        payload = {"content": "a" * 10, "rating": 5}

        authenticated_api_client.post(f"/api/products/{product_id}/reviews/", payload)
        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", payload
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_if_data_is_valid_returns_201(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        payload = {"content": "a" * 10, "rating": 5}

        response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", payload
        )
        result = response.data

        assert response.status_code == status.HTTP_201_CREATED

        assert result["content"] == payload["content"]
        assert result["rating"] == payload["rating"]


@pytest.mark.django_db
class TestRetrieveProductReview:
    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get("/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(self, api_client, create_product):
        product_id = create_product.id
        response = api_client.get(f"/api/products/{product_id}/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_exists_returns_200(self, api_client, create_product_review):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = api_client.get(f"/api/products/{product_id}/reviews/{review_id}/")
        result = response.data

        assert response.status_code == status.HTTP_200_OK

        assert result["id"] == review_id
        assert result["rating"] == create_product_review.rating
        assert result["content"] == create_product_review.content


@pytest.mark.django_db
class TestUpdateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_review):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, create_product_review
    ):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.put(f"/api/products/1/reviews/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/1/", {}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        create_payload = {"content": "a" * 10, "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", create_payload
        )

        review_id = create_response.data["id"]
        update_response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        create_payload = {"content": "a" * 10, "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", create_payload
        )

        review_id = create_response.data["id"]
        update_payload = {"content": "b" * 10, "rating": 9}
        update_response = authenticated_api_client.put(
            f"/api/products/{product_id}/reviews/{review_id}/", update_payload
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["content"] == update_payload["content"]
        assert update_response.data["rating"] == update_payload["rating"]


@pytest.mark.django_db
class TestPartialUpdateProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_review):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = api_client.patch(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, create_product_review
    ):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = authenticated_api_client.patch(
            f"/api/products/{product_id}/reviews/{review_id}/", {}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.patch(f"/api/products/1/reviews/1/", {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        response = authenticated_api_client.patch(
            f"/api/products/{product_id}/reviews/1/", {}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_data_is_invalid_returns_400(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        create_payload = {"content": "a" * 10, "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", create_payload
        )

        review_id = create_response.data["id"]
        update_payload = {"rating": 0}
        update_response = authenticated_api_client.patch(
            f"/api/products/{product_id}/reviews/{review_id}/", update_payload
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        create_payload = {"content": "a" * 10, "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", create_payload
        )

        review_id = create_response.data["id"]
        update_payload = {"rating": 1}
        update_response = authenticated_api_client.patch(
            f"/api/products/{product_id}/reviews/{review_id}/", update_payload
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["content"] == create_payload["content"]
        assert update_response.data["rating"] == update_payload["rating"]


@pytest.mark.django_db
class TestDeleteProductReview:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product_review):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = api_client.delete(f"/api/products/{product_id}/reviews/{review_id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_author_returns_403(
        self, authenticated_api_client, create_product_review
    ):
        product_id = create_product_review.product.id
        review_id = create_product_review.id

        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{review_id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticated_api_client):
        response = authenticated_api_client.delete(f"/api/products/1/reviews/1/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_review_does_not_exist_returns_404(
        self, authenticated_api_client, create_product
    ):
        product_id = create_product.id
        response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/1/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_is_author_returns_204(
        self,
        authenticated_api_client,
        create_product,
    ):
        product_id = create_product.id
        create_payload = {"content": "a" * 10, "rating": 5}
        create_response = authenticated_api_client.post(
            f"/api/products/{product_id}/reviews/", create_payload
        )

        review_id = create_response.data["id"]
        delete_response = authenticated_api_client.delete(
            f"/api/products/{product_id}/reviews/{review_id}/"
        )

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(id=review_id).exists()
