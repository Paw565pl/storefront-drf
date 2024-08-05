from django_filters import rest_framework as filters

from products.models import Product, Review


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ["title", "unit_price", "inventory", "last_update", "collection"]

    title = filters.CharFilter(lookup_expr="icontains")
    unit_price = filters.RangeFilter()
    inventory = filters.RangeFilter()
    last_update = filters.DateRangeFilter()


class ReviewFilter(filters.FilterSet):
    class Meta:
        model = Review
        fields = ["rating", "created_at"]

    rating = filters.RangeFilter()
    created_at = filters.DateRangeFilter()
