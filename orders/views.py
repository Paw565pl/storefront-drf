from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from orders.models import CustomerAddress, Cart, CartItem, Order, Customer
from orders.serializers import (
    CustomerAddressSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    UpdateCartItemSerializer,
    CreateCartItemSerializer,
    CreateOrderSerializer,
    UpdateOrderSerializer,
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

    def get_queryset(self):
        cart_id = self.kwargs["cart_pk"]
        cart = get_object_or_404(Cart, id=cart_id)

        return (
            CartItem.objects.filter(cart_id=cart)
            .select_related("product")
            .order_by("id")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCartItemSerializer
        elif self.action == "partial_update":
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_id = self.kwargs["cart_pk"]
        get_object_or_404(Cart, id=cart_id)
        return super().create(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options", "trace"]

    def get_queryset(self):
        queryset = (
            Order.objects.select_related("address")
            .prefetch_related("orderitem_set__product")
            .order_by("id")
        )

        user = self.request.user
        if user.is_staff:
            return queryset

        customer_id = Customer.objects.only("id").get(user_id=user.id)
        return queryset.filter(customer_id=customer_id)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer
        elif self.action == "partial_update":
            return UpdateOrderSerializer
        else:
            return OrderSerializer

    def get_permissions(self):
        if self.action in ["partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
