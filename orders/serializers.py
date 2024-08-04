from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import Customer, CustomerAddress, CartItem, Cart
    OrderAddress,
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
        fields = ["id", "product", "quantity", "total_price"]
        read_only_fields = ["quantity", "total_price"]

    product = SimpleProductSerializer(read_only=True)

    @staticmethod
    def validate_quantity_in_stock(quantity: int, product: Product):
        if quantity > product.inventory:
            raise serializers.ValidationError(
                "You cannot add more to your cart than is available in stock."
            )


class CreateCartItemSerializer(CartItemSerializer):
    class Meta:
        model = CartItem
        fields = ["product_id", "quantity"]

    product_id = serializers.IntegerField(write_only=True)

    @staticmethod
    def validate_product_id(product_id: int):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Invalid product id.")
        return product_id

    def create(self, validated_data):
        cart_id = self.context["view"].kwargs["cart_pk"]
        quantity = validated_data["quantity"]

        product_id = validated_data["product_id"]
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

    def to_representation(self, instance: CartItem):
        return CartItemSerializer(context=self.context).to_representation(instance)


class UpdateCartItemSerializer(CartItemSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    def update(self, instance: CartItem, validated_data):
        quantity = validated_data.get("quantity")
        if quantity is None:
            raise serializers.ValidationError({"quantity": ["This field is required."]})

        product = instance.product
        self.validate_quantity_in_stock(quantity, product)

        instance.quantity = quantity
        instance.total_price = quantity * product.unit_price
        instance.save()

        return instance

    def to_representation(self, instance: CartItem):
        return CartItemSerializer(context=self.context).to_representation(instance)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
        read_only_fields = ["total_price"]

    items = CartItemSerializer(read_only=True, many=True, source="cartitem_set")


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]
        extra_kwargs = {
            "quantity": {"read_only": True},
            "total_price": {"read_only": True},
        }

    product = SimpleProductSerializer(read_only=True)
