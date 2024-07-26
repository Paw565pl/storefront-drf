from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from orders.models import CustomerAddress, Cart
from orders.serializers import CustomerAddressSerializer, CartSerializer


# Create your views here.
class CustomerAddressView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerAddress.objects.filter(customer__user_id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(), customer__user_id=self.request.user.id
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("cartitem_set__product").all()
    serializer_class = CartSerializer
