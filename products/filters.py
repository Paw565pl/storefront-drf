from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    unit_price = filters.RangeFilter()
    inventory = filters.RangeFilter()
    last_update = filters.DateRangeFilter()

    class Meta:
        model = Product
        fields = ["title", "unit_price", "inventory", "last_update", "collection"]
