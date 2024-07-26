from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import Customer, CustomerAddress, CartItem
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
    def validate_product_id(product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Invalid product id.")
        return product_id
