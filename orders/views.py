from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from orders.models import CustomerAddress, Cart, CartItem
from orders.serializers import (
    CustomerAddressSerializer,
    CartSerializer,
    CartItemSerializer,
)


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


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options", "trace"]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs["cart_pk"]
        cart = get_object_or_404(Cart, id=cart_id)

        return (
            CartItem.objects.filter(cart_id=cart)
            .select_related("product")
            .order_by("id")
            .all()
        )

    def create(self, request, *args, **kwargs):
        cart_id = self.kwargs["cart_pk"]
        get_object_or_404(Cart, id=cart_id)
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=inline_serializer(
            "CartItemUpdatePayload",
            fields={"quantity": serializers.IntegerField(min_value=1)},
        )
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
