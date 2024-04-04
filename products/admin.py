from typing import Any

from django.contrib import admin, messages
from django.db.models import QuerySet, Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django_admin_inline_paginator.admin import TabularInlinePaginated

from products.models import Product, ProductImage, Collection, Review


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"
    filter_values = [("<10", "Low"), (">=10", "Ok")]

    def lookups(self, request, model_admin):
        return self.filter_values

    def queryset(self, request, queryset: QuerySet[Any]):
        if self.value() == self.filter_values[0][0]:
            return queryset.filter(inventory__lt=10)
        elif self.value() == self.filter_values[1][0]:
            return queryset.filter(inventory__gte=10)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title__icontains"]
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:products_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))


class ProductImageInline(TabularInlinePaginated):
    model = ProductImage
    readonly_fields = ["thumbnail"]

    per_page = 3
    extra = 1

    @staticmethod
    def thumbnail(instance: ProductImage):
        if instance.image.name != "":
            return format_html(f"<img src='{instance.image.url}' width='50px'/>")
        return ""


class ProductReviewInline(TabularInlinePaginated):
    model = Review
    readonly_fields = ["author", "created_at"]

    per_page = 3
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    search_fields = ["title__icontains"]
    readonly_fields = ["slug", "last_update"]
    actions = ["clear_inventory"]
    inlines = [ProductImageInline, ProductReviewInline]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 20
    list_select_related = ["collection"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    @staticmethod
    def collection_title(product):
        return product.collection.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset: QuerySet[Any]):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated",
            messages.SUCCESS,
        )
