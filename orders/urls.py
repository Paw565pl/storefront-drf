from django.urls import path, include
from rest_framework_nested import routers

from orders.views import CustomerAddressView, CartViewSet

router = routers.DefaultRouter()
router.register(r"carts", CartViewSet, basename="carts")

urlpatterns = [
    path("", include(router.urls)),
    path("orders/address", CustomerAddressView.as_view(), name="customer-address"),
]
