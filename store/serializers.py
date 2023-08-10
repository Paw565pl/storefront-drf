from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.SerializerMethodField(method_name="get_products_count")

    def get_products_count(self, collection: Collection):
        return collection.product_set.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "price_with_tax",
            "inventory",
            "collection",
            "promotions",
        ]

    # price = serializers.DecimalField(
    #     max_digits=10, decimal_places=2, min_value=0, source="unit_price"
    # )
    price_with_tax = serializers.SerializerMethodField(
        method_name="calculate_price_with_tax"
    )
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(), view_name="collection_detail"
    # )

    def calculate_price_with_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.23), 2)
