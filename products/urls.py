from django.urls import path, include
from rest_framework_nested import routers

from products.views import (
    ProductViewSet,
    ProductImageViewSet,
    ProductReviewViewSet,
    CollectionViewSet,
    ProductVoteView,
    ProductReviewVoteView,
)

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"collections", CollectionViewSet, basename="collections")

product_router = routers.NestedSimpleRouter(router, r"products", lookup="product")
product_router.register(r"images", ProductImageViewSet, basename="product-images")
product_router.register(r"reviews", ProductReviewViewSet, basename="product-reviews")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("products/<product_pk>/vote/", ProductVoteView.as_view()),
    path(
        "products/<product_pk>/reviews/<pk>/vote/",
        ProductReviewVoteView.as_view(),
    ),
]
