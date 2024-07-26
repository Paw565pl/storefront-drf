from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from orders.models import Customer, CustomerAddress


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
