from django.urls import path, include
from rest_framework_nested import routers

from products.views import ProductViewSet, ProductImageViewSet

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")

product_router = routers.NestedSimpleRouter(router, r"products", lookup="product")
product_router.register(r"images", ProductImageViewSet, basename="product-images")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
]
