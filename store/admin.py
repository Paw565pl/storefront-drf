from typing import Any, List, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from .models import *


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"
    filter_values = [("<10", "Low")]

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return self.filter_values

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == self.filter_values[0][0]:
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance: ProductImage):
        if instance.image.name != "":
            return format_html(f"<img src='{instance.image.url}' width='50px'/>")
        return ""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    search_fields = ["title__istartswith", "description__istartswith"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    inlines = [ProductImageInline]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Ok"

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request: Any, queryset: QuerySet[Any]):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated",
            messages.SUCCESS,
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "users_id",
        "first_name",
        "last_name",
        "membership",
        "phone",
        "birth_date",
    ]
    list_editable = ["membership"]
    list_per_page = 10
    list_select_related = ["user"]
    autocomplete_fields = ["user"]
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]

    @admin.display(ordering="user__id")
    def users_id(self, customer):
        return customer.user.id

    @admin.display(ordering="user__first_name")
    def first_name(self, customer):
        return customer.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self, customer):
        return customer.user.last_name


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ["product"]
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "payment_status", "customer"]
    list_select_related = ["customer"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ["title__istartswith"]
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count("product"))
