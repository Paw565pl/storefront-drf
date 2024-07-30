from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import Customer, CustomerAddress, CartItem, Cart
from products.models import Product
from products.serializers import SimpleProductSerializer


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "apartment_number",
            "street_number",
            "street",
            "postal_code",
            "city",
            "state",
            "country",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        customer = get_object_or_404(Customer, user=user)

        if customer.address:
            raise serializers.ValidationError("Customer already has an address.")

        created_address = super().create(validated_data)
        customer.address = created_address
        customer.save()

        return created_address


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "product", "quantity", "total_price"]

    product_id = serializers.IntegerField(write_only=True)
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )

    @staticmethod
    def validate_product_id(product_id: int):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Invalid product id.")
        return product_id

    @staticmethod
    def validate_quantity_in_stock(quantity: int, product: Product):
        if quantity > product.inventory:
            raise serializers.ValidationError(
                "You cannot add more to your cart than is available in stock."
            )

    def create(self, validated_data):
        cart_id = self.context["view"].kwargs["cart_pk"]
        quantity = self.validated_data["quantity"]

        product_id = self.validated_data["product_id"]
        product = Product.objects.only("unit_price", "inventory").get(id=product_id)

        self.validate_quantity_in_stock(quantity, product)

        try:
            # update existing cart item quantity and total_price
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.total_price = quantity * cart_item.product.unit_price
            cart_item.save()

            return cart_item
        except CartItem.DoesNotExist:
            total_price = quantity * product.unit_price
            return CartItem.objects.create(
                cart_id=cart_id, total_price=total_price, **self.validated_data
            )

    def update(self, instance: CartItem, validated_data):
        quantity = self.validated_data.get("quantity")
        if quantity is None:
            raise serializers.ValidationError({"quantity": ["This field is required."]})

        product = instance.product
        self.validate_quantity_in_stock(quantity, product)

        instance.quantity = quantity
        instance.total_price = quantity * product.unit_price
        instance.save()

        return instance


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    items = CartItemSerializer(many=True, read_only=True, source="cartitem_set")
    total_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]
        extra_kwargs = {
            "quantity": {"read_only": True},
            "total_price": {"read_only": True},
        }

    product = SimpleProductSerializer(read_only=True)
