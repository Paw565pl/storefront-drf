from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter
from products.mixins import MultipleFieldLookupMixin
from products.models import Product, ProductImage
from products.permissions import IsAdminOrReadOnly
from products.serializers import ProductSerializer, ProductImageSerializer


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
    ordering_fields = ["id"]

    def get_queryset(self):
        product_id = self.kwargs["product_pk"]
        get_object_or_404(Product, pk=product_id)
        return ProductImage.objects.filter(product=self.kwargs["product_pk"]).order_by("id")

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs["product_pk"]
        get_object_or_404(Product, pk=product_id)
        return super().create(request, *args, **kwargs)
