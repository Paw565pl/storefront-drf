from rest_framework import serializers

from products.models import Collection, ProductImage, Review, Product, Promotion


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.SerializerMethodField()

    @staticmethod
    def get_products_count(collection: Collection):
        return collection.product_set.count()


class SimpleCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def create(self, validated_data):
        product_id = self.context["view"].kwargs["product_pk"]
        return ProductImage.objects.create(product_id, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author", "rating", "content", "created_at"]

    def create(self, validated_data):
        product_id = self.context["view"].kwargs["product_pk"]
        return Review.objects.create(product_id, **validated_data)


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "description", "discount"]


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
            "collection",
            "collection_id",
            "promotions",
            "images",
        ]

    slug = serializers.SlugField(read_only=True)
    collection = SimpleCollectionSerializer(read_only=True)
    collection_id = serializers.IntegerField(write_only=True)
    images = ProductImageSerializer(
        source="productimage_set", many=True, read_only=True
    )
    promotions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        collection_id = validated_data.get("collection_id")
        collection_exists = Collection.objects.filter(id=collection_id).exists()

        if not collection_exists:
            raise serializers.ValidationError("Collection does not exist.")

        return Product.objects.create(**validated_data)

    def update(self, instance: Product, validated_data):
        collection_id = validated_data.get("collection_id")
        collection_exists = Collection.objects.filter(id=collection_id).exists()

        if not collection_exists:
            raise serializers.ValidationError("Collection does not exist.")

        return super().update(instance, validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "unit_price"]
