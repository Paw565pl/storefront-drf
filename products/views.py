from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter, ReviewFilter
from products.mixins import MultipleFieldLookupMixin
from products.models import Product, ProductImage, Review
from products.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from products.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ReviewSerializer,
)
from products.utils import get_product_or_404


# Create your views here.
class ProductViewSet(MultipleFieldLookupMixin, ModelViewSet):
    queryset = (
        Product.objects.select_related("collection")
        .prefetch_related("promotions")
        .prefetch_related("productimage_set")
        .all()
    )
    serializer_class = ProductSerializer
    lookup_fields = ["id", "slug"]
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    ordering_fields = ["title", "unit_price", "inventory", "last_update"]

    @method_decorator([cache_page(60 * 5), vary_on_cookie])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = []

    def get_queryset(self):
        product_identifier = self.kwargs["product_pk"]
        product = get_product_or_404(product_identifier)
        return ProductImage.objects.filter(product=product).order_by("id")

    def create(self, request, *args, **kwargs):
        product_identifier = self.kwargs["product_pk"]
        get_product_or_404(product_identifier)
        return super().create(request, *args, **kwargs)


class ProductReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_class = ReviewFilter
    ordering_fields = ["rating", "created_at"]

    def get_queryset(self):
        product_identifier = self.kwargs["product_pk"]
        product = get_product_or_404(product_identifier)
        return Review.objects.filter(product=product)

    def create(self, request, *args, **kwargs):
        product_identifier = self.kwargs["product_pk"]
        get_product_or_404(product_identifier)
        return super().create(request, *args, **kwargs)
