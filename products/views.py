from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter
from products.mixins import MultipleFieldLookupMixin
from products.models import Product
from products.permissions import IsAdminOrReadOnly
from products.serializers import ProductSerializer


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
