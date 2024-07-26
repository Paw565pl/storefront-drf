from django.urls import path, include
from rest_framework_nested import routers

from orders.views import CustomerAddressView, CartViewSet, CartItemViewSet

router = routers.SimpleRouter()
router.register(r"carts", CartViewSet, basename="carts")

cart_router = routers.NestedSimpleRouter(router, r"carts", lookup="cart")
cart_router.register(r"items", CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("orders/address", CustomerAddressView.as_view(), name="customer-address"),
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
]
