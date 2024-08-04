from django.urls import path, include
from rest_framework_nested import routers

from orders.views import CustomerAddressView, CartViewSet, CartItemViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r"carts", CartViewSet, basename="carts")
router.register(r"orders", OrderViewSet, basename="orders")

cart_router = routers.NestedSimpleRouter(router, r"carts", lookup="cart")
cart_router.register(r"items", CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("address/", CustomerAddressView.as_view(), name="customer-address"),
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
]
