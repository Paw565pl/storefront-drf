from django.db import IntegrityError
from rest_framework import serializers

from core.exceptions import Conflict
from products.models import Collection, ProductImage, Review, Product, Promotion
from products.utils import get_product_or_404


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class SimpleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def create(self, validated_data):
        product_identifier = self.context["view"].kwargs["product_pk"]
        product = get_product_or_404(product_identifier)
        return ProductImage.objects.create(product=product, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "author",
            "rating",
            "content",
            "created_at",
            "likes_count",
            "dislikes_count",
        ]

    author = serializers.CharField(read_only=True, source="author.username")
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        product_identifier = self.context["view"].kwargs["product_pk"]
        product = get_product_or_404(product_identifier)

        try:
            return Review.objects.create(author=user, product=product, **validated_data)
        except IntegrityError:
            raise Conflict("You have already reviewed this product.")


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name", "discount"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "unit_price",
            "inventory",
            "last_update",
            "likes_count",
            "dislikes_count",
            "collection",
            "collection_id",
            "promotions",
            "images",
        ]

    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)

    collection = SimpleCollectionSerializer(read_only=True)
    collection_id = serializers.IntegerField(write_only=True)

    images = ProductImageSerializer(
        read_only=True, many=True, source="productimage_set"
    )
    promotions = PromotionSerializer(read_only=True, many=True)

    @staticmethod
    def validate_collection_id(collection_id: int):
        if not Collection.objects.filter(id=collection_id).exists():
            raise serializers.ValidationError(
                "Collection with given id does not exist."
            )
        return collection_id


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "unit_price", "inventory"]
