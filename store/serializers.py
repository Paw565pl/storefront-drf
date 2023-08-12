from rest_framework import serializers
from decimal import Decimal
from .models import CartItem, Product, Collection, Review, Cart, Customer


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "date"]

    def create(self, validated_data):
        product_id = self.context["product_pk"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart_item: CartItem):
        return round(cart_item.product.unit_price * cart_item.quantity, 2)


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Invalid product id")
        return product_id

    def save(self, **kwargs):
        cart_id = self.context["cart_pk"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "cart_items", "total_price"]

    id = serializers.UUIDField(read_only=True)
    cart_items = CartItemSerializer(many=True, source="cartitem_set", read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart: Cart):
        total_price = 0
        for cart_item in cart.cartitem_set.all():
            total_price += cart_item.product.unit_price * cart_item.quantity
        return round(total_price, 2)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "membership",
        ]

    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.SerializerMethodField(
        method_name="get_first_name", read_only=True
    )
    last_name = serializers.SerializerMethodField(
        method_name="get_last_name", read_only=True
    )

    def get_first_name(self, customer: Customer):
        return customer.user.first_name

    def get_last_name(self, customer: Customer):
        return customer.user.last_name
