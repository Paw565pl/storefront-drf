from django.urls import path

from orders.views import CustomerAddressView

urlpatterns = [
    path("orders/address", CustomerAddressView.as_view(), name="customer-address"),
]
